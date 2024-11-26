import logging

from datetime import datetime
from django.db.transaction import atomic

from academy.models import CourseProgress, Product

from .models import ChapterCompleted
from .helpers import get_or_create_student

db_logger = logging.getLogger('db')


def ezycourse_chapter_completed(data: dict):
    """
    This webhook is triggered when a new user signs up.
    """
    try:
        obj: ChapterCompleted = ChapterCompleted.from_json(data)
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

        cc.current_chapter_id = obj.chapter_name
        cc.last_viewed = datetime.now()
        cc.save()

        db_logger.info(f"Chapter {obj.chapter_name} completed by {st}")


__all__ = ("ezycourse_chapter_completed",)
