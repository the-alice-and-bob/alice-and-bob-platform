import logging

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
            scheduled_at=timezone.now().date(),
    ).first():
        return email_for_today

    # If there are no emails planned to be sent today, return the first email on the queue. We prioritize older emails. field: created
    return EmailCampaigns.objects.filter(
        is_sent=False,
    ).order_by('created').first()


def create_send_campaign_email(email_campaign_id: int | EmailCampaigns):
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

    if isinstance(email_campaign_id, EmailCampaigns):
        instance = email_campaign_id

    else:
        try:
            instance = EmailCampaigns.objects.get(pk=email_campaign_id)
        except EmailCampaigns.DoesNotExist:
            raise Exception(f"Email campaign not found with id {email_campaign_id}")

    acu = AcumbamailAPI()
    ret = acu.send_many(
        campaign_name=f"[{timezone.now().today().strftime('%Y-%m-%d')}] {instance.subject}",
        subject=instance.subject,
        body=instance.content,
        scheduled_date=instance.scheduled_at,
        list_id=instance.mail_list.acumbamail_id,
    )

    instance.campaign_id = ret
    instance.save()


def send_daily_email():
    """
    The purpose of this function is to send a daily email to the mail list.
    """
    email = choice_daily_email()

    if not email:
        return

    with atomic():
        email.is_sent = True
        email.send_date = timezone.now()

        create_send_campaign_email(email)


__all__ = ('create_send_campaign_email', 'send_daily_email')
