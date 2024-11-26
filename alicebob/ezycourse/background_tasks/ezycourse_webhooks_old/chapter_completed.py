from .models import ChapterCompleted
from .helpers import update_course_progress


def ezycourse_chapter_completed(data: dict):
    """
    This webhook is triggered when a new user signs up.
    """
    try:
        obj: ChapterCompleted = ChapterCompleted.from_json(data)
    except Exception as e:
        raise ValueError(f"Invalid data: {e}")

    update_course_progress(obj)


__all__ = ("ezycourse_chapter_completed",)
