import logging

from campaigns.models import MailList
from campaigns.sdk import AcumbamailAPI

DEFAULT_MAIL_LIST_NAME = "alicebob-all-users"

logger = logging.getLogger("db")


def subscribe_user_to_mail_list(name: str, email: str):
    try:
        mail_list = MailList.objects.get(name=DEFAULT_MAIL_LIST_NAME)
    except MailList.DoesNotExist:
        logger.error(f"Mail list {DEFAULT_MAIL_LIST_NAME} does not exist")
        return

    ac = AcumbamailAPI()
    ac.add_subscriber(email=email, name=name, list_id=mail_list.id)

    logger.info(f"User {name} subscribed to mail list {mail_list.name}")
