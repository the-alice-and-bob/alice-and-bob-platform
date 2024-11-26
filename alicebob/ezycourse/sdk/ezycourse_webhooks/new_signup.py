import logging

from .models import NewSignup
from .helpers import get_or_create_student

db_logger = logging.getLogger('db')


def ezycourse_new_signup(data: dict):
    """
    This webhook is triggered when a new user signs up.
    """
    try:
        obj = NewSignup.from_json(data)
    except Exception as e:
        db_logger.error(f"Invalid data while processing new signup: {e}")
        return

    get_or_create_student(obj)

    db_logger.info(f"Student {obj.email} signed up")


__all__ = ("ezycourse_new_signup",)
