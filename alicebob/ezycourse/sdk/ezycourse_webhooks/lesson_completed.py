from datetime import datetime

from django.db.transaction import atomic

from academy.models import CourseProgress, Product

from .models import LessonCompleted
from .helpers import get_or_create_student


def ezycourse_lesson_completed(data: dict):
    """
    This webhook is triggered when a new user signs up.
    """
    try:
        obj = LessonCompleted.from_json(data)
    except Exception as e:
        raise ValueError(f"Invalid data: {e}")

    st = get_or_create_student(obj)

    with atomic():
        try:
            course = Product.objects.get(ezy_id=obj.course_id)
        except Product.DoesNotExist:
            print(f"Course {obj.course_id} not found in the DB")
            return

        try:
            cc = CourseProgress.objects.get(student=st, course=course)
        except CourseProgress.DoesNotExist:
            cc = CourseProgress.objects.create(student=st, course=course)

        cc.current_lesson = obj.lesson_name
        cc.last_viewed = datetime.now()
        cc.save()

        print(f"Lesson {obj.lesson_name} completed by {st}")

__all__ = ("ezycourse_lesson_completed",)
