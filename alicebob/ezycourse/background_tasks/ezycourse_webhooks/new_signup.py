from .models import NewSignup
from .helpers import check_or_create_student


def ezycourse_new_signup(data: dict):
    """
    This webhook is triggered when a new user signs up.
    """
    try:
        obj = NewSignup.from_json(data)
    except Exception as e:
        raise ValueError(f"Invalid data: {e}")

    try:
        check_or_create_student(
            email=obj.email,
            identifier=obj.identifier,
            first_name=obj.first_name,
            last_name=obj.last_name,
        )
    except Exception as e:
        print(f"Error creating student: {e}")



__all__ = ("ezycourse_new_signup",)
