from .models import CourseCompleted
from .helpers import update_course_progress


def ezycourse_course_completed(data: dict):
    """
    This webhook is triggered when a new user signs up.
    """
    try:
        obj = CourseCompleted.from_json(data)
    except Exception as e:
        raise ValueError(f"Invalid data: {e}")

    update_course_progress(obj)

__all__ = ("ezycourse_course_completed",)
