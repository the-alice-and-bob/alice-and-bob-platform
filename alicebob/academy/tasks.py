"""
This file contains the tasks that are triggered by the EzyCourses webhooks:
"""

from celery import shared_task

from .background_tasks.models import *


@shared_task
def new_signup(info: dict):
    try:
        obj = NewSignup.from_json(info)
    except Exception as e:
        print(f"Error while processing new signup: {e}")
        return False


@shared_task
def new_product_enrollment(info: dict):
    try:
        obj = NewProduct.from_json(info)
    except Exception as e:
        print(f"Error while processing new product enrollment: {e}")
        return False


@shared_task
def new_sale(info: dict):
    try:
        obj = NewProduct.from_json(info)
    except Exception as e:
        print(f"Error while processing new sale: {e}")
        return False


@shared_task
def course_completed(info: dict):
    try:
        obj = CourseCompleted.from_json(info)
    except Exception as e:
        print(f"Error while processing course completed: {e}")
        return False


@shared_task
def chapter_completed(info: dict):
    try:
        obj = ChapterCompleted.from_json(info)
    except Exception as e:
        print(f"Error while processing chapter completed: {e}")
        return False


@shared_task
def quiz_completed(info: dict):
    try:
        obj = QuizCompleted.from_json(info)
    except Exception as e:
        print(f"Error while processing quiz completed: {e}")
        return False


@shared_task
def lesson_completed(info: dict):
    try:
        obj = LessonCompleted.from_json(info)
    except Exception as e:
        print(f"Error while processing lesson completed: {e}")
        return False
