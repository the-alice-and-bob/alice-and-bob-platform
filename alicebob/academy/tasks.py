"""
This file contains the tasks that are triggered by the EzyCourses webhooks:
"""

from celery import shared_task

from .background_tasks import *


@shared_task(name="task_ezycourse_new_signup")
def task_ezycourse_new_signup(info: dict):
    try:
        ezycourse_new_signup(info)
    except Exception as e:
        print(f"Error while processing new signup: {e}")
        return False


@shared_task(name="task_ezycourse_new_product_enrollment")
def task_ezycourse_new_product_enrollment(info: dict):
    try:
        ezycourse_new_product_enrollment(info)
    except Exception as e:
        print(f"Error while processing new product enrollment: {e}")
        return False


@shared_task(name="task_ezycourse_new_sale")
def task_ezycourse_new_sale(info: dict):
    try:
        ezycourse_new_sale(info)
    except Exception as e:
        print(f"Error while processing new sale: {e}")
        return False


@shared_task(name="task_ezycourse_course_completed")
def task_ezycourse_course_completed(info: dict):
    try:
        ezycourse_course_completed(info)
    except Exception as e:
        print(f"Error while processing course completed: {e}")
        return False


@shared_task(name="task_ezycourse_chapter_completed")
def task_ezycourse_chapter_completed(info: dict):
    try:
        ezycourse_chapter_completed(info)
    except Exception as e:
        print(f"Error while processing chapter completed: {e}")
        return False


@shared_task(name="task_ezycourse_quiz_completed")
def task_ezycourse_quiz_completed(info: dict):
    try:
        ezycourse_quiz_completed(info)
    except Exception as e:
        print(f"Error while processing quiz completed: {e}")
        return False


@shared_task(name="task_ezycourse_lesson_completed")
def task_ezycourse_lesson_completed(info: dict):
    try:
        ezycourse_lesson_completed(info)
    except Exception as e:
        print(f"Error while processing lesson completed: {e}")
        return False
