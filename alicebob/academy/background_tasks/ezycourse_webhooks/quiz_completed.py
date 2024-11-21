from .models import QuizCompleted


def ezycourse_quiz_completed(data: dict):
    """
    This webhook is triggered when a new user signs up.
    """
    try:
        obj = QuizCompleted.from_json(data)
    except Exception as e:
        raise ValueError(f"Invalid data: {e}")


__all__ = ("ezycourse_quiz_completed",)
