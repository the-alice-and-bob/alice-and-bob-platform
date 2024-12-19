import logging

from django.db.transaction import atomic

from campaigns.models import MailList
from campaigns.sdk import AcumbamailAPI
from academy.models import Student, Lead

DEFAULT_MAIL_LIST_NAME = "alicebob-all-users"

logger = logging.getLogger("db")


def subscribe_user_to_mail_list(name: str, email: str):
    try:
        mail_list = MailList.objects.get(name=DEFAULT_MAIL_LIST_NAME)
    except MailList.DoesNotExist:
        logger.error(f"[!!!!] Mail list {DEFAULT_MAIL_LIST_NAME} does not exist")
        return

    lead = user = None
    try:
        # Get the user from the mail list
        user = Student.objects.get(email=email)
    except Student.DoesNotExist:
        try:
            # Get the user from the leads
            lead = Lead.objects.get(email=email)
        except Lead.DoesNotExist:
            logger.info(f"User {name} with email {email} does not exist in the database. Creating a lead")
            lead = Lead.objects.create(email=email)

    with atomic():

        # Check if the user is already subscribed
        if user:
            if mail_list.users.filter(pk=user.pk).exists():
                logger.info(f"User {name} is already subscribed to mail list {mail_list.name}")
                return

            else:
                mail_list.users.add(user)
                mail_list.subscribers += 1
                mail_list.save()

        if lead:
            if mail_list.leads.filter(pk=lead.pk).exists():
                logger.info(f"Lead {name} is already subscribed to mail list {mail_list.name}")
                return

            else:
                mail_list.leads.add(lead)
                mail_list.subscribers += 1
                mail_list.save()

        ac = AcumbamailAPI()
        ac.add_subscriber(email=email, name=name, list_id=mail_list.acumbamail_id)

        logger.info(f"User {name} subscribed to mail list {mail_list.name}")
