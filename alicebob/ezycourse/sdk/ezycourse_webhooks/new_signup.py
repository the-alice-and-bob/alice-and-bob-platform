from .models import NewSignup
from .helpers import get_or_create_student


def ezycourse_new_signup(data: dict):
    """
    This webhook is triggered when a new user signs up.
    """
    try:
        obj = NewSignup.from_json(data)
    except Exception as e:
        raise ValueError(f"Invalid data: {e}")

    get_or_create_student(obj)

    print(f"Student {obj.email} signed up")


__all__ = ("ezycourse_new_signup",)
