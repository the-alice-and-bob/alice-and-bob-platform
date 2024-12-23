import random
import logging

from django.conf import settings
from django.utils import timezone

from django.db.transaction import atomic

from ..models import MailList, EmailCampaigns
from ..sdk import AcumbamailAPI

logger = logging.getLogger("db")


def choice_daily_email() -> EmailCampaigns:
    """
    The purpose of this function is to choice an email to send daily.

    The algorithm is the following:

    - Check if there are emails planned to be sent today
    - If there are emails planned to be sent today, return the first email planned to be sent today
    - If there are no emails planned to be sent today, return the first email on the queue
    """

    # Check if there are emails planned to be sent today, if so, return the first email planned to be sent today
    if email_for_today := EmailCampaigns.objects.filter(
            is_sent=False,
            is_draft=False,
            # Cualquiera que esté planificado para hoy. Coger el primero
            scheduled_at=timezone.now().today()
    ).first():
        return email_for_today

    # If not email for today, then check the day of the week is: monday, tuesday, wednesday, thursday, friday, saturday, sunday.
    # And return the first email planned to be sent today
    day_of_the_week = timezone.now().today().strftime('%A').lower()

    if email_for_today := EmailCampaigns.objects.filter(
            is_sent=False,
            is_draft=False,
            # Cualquiera que esté planificado para hoy
            preferred_day=day_of_the_week
    ).first():
        return email_for_today

    # If there are no emails planned to be sent today, return the first email on the queue. We prioritize older emails. field: created
    return EmailCampaigns.objects.filter(
        is_draft=False,
        is_sent=False,
    ).order_by('created').first()


def create_send_campaign_email(email_campaign_id: int | EmailCampaigns, auto_save: bool = True):
    """
    Creates and sends an email campaign using the specified campaign ID or an EmailCampaigns instance.

    If an integer campaign ID is provided, the method attempts to retrieve the corresponding
    EmailCampaigns instance. If the campaign is not found, an exception is raised. If an
    EmailCampaigns instance is directly provided, it is used for sending the campaign email.

    The email campaign is sent using the Acumbamail API, and the campaign ID returned is saved
    to the `campaign_id` attribute of the corresponding EmailCampaigns instance.

    :param email_campaign_id: The campaign identifier, either an integer ID corresponding to a database entry or an EmailCampaigns instance.
    :type email_campaign_id: int | EmailCampaigns
    :return: None
    """
    if not email_campaign_id:
        logger.error(f"Invalid email campaign ID: {email_campaign_id}")
        return

    if isinstance(email_campaign_id, EmailCampaigns):
        instance = email_campaign_id

    else:
        try:
            instance = EmailCampaigns.objects.get(pk=email_campaign_id)
        except EmailCampaigns.DoesNotExist:
            raise Exception(f"Email campaign not found with id {email_campaign_id}")

    if not settings.DEBUG:
        acu = AcumbamailAPI()
        ret = acu.send_many(
            campaign_name=f"[{timezone.now().today().strftime('%Y-%m-%d')}] {instance.subject}",
            subject=instance.subject,
            body=instance.content,
            scheduled_date=instance.scheduled_at,
            list_id=instance.mail_list.acumbamail_id,
        )
    else:
        ret = random.randint(1, 9000)

    try:
        ret = int(ret)
    except ValueError:
        logger.error(f"Invalid campaign ID returned from Acumbamail: {ret}")
        return

    instance.acumbamail_id = ret

    if auto_save:
        instance.save()


def send_daily_email():
    """
    The purpose of this function is to send a daily email to the mail list.
    """
    email = choice_daily_email()

    if not email:
        return

    with atomic():
        create_send_campaign_email(email, auto_save=False)

        email.is_sent = True
        email.send_date = timezone.now()
        email.save()


__all__ = ('create_send_campaign_email', 'send_daily_email')
