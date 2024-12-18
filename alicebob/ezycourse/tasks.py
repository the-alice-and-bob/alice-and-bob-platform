"""
This file contains the tasks that are triggered by the EzyCourses webhooks:
"""

from celery import shared_task

from .engine import subscribe_user_to_mail_list


@shared_task(name="task_subscribe_new_user_to_general_list", ignore_result=True)
def task_subscribe_new_user_to_general_list(name: str, email: str):
    subscribe_user_to_mail_list(name, email)
