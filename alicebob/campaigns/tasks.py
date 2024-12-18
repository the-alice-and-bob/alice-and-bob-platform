"""
This file contains the tasks that are triggered by the EzyCourses webhooks:
"""
from celery import shared_task

from .engine import *
from .sdk import sync_list_from_acumbamail


# -------------------------------------------------------------------------
# Tasks for the Acumbamail when a new student is created or a new
# product is created
# -------------------------------------------------------------------------
@shared_task(name="task_create_purchase_order", rate_limit="30/m", ignore_result=True)
def task_create_purchase_order(sell_id: int):
    """
    This task creates a purchase order in Acumbamail
    """
    create_purchase_order(sell_id)


@shared_task(name="task_create_student", rate_limit="30/m", ignore_result=True)
def task_create_student(student_id: int):
    create_student(student_id)


@shared_task(name="task_create_product", rate_limit="30/m", ignore_result=True)
def task_create_product(product_id: int):
    create_product(product_id)


@shared_task(name="task_create_send_campaign_email", rate_limit="60/m", ignore_result=True)
def task_create_send_campaign_email(daily_email_id: int):
    create_send_campaign_email(daily_email_id)


# -------------------------------------------------------------------------
# End of tasks for the Acumbamail list management
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# Tasks for webhooks
# -------------------------------------------------------------------------
@shared_task(name="task_process_acumbamail_webhook", ignore_result=True)
def task_process_acumbamail_webhook(list_id, email, timestamp, event_type):
    handle_action(list_id, email, timestamp, event_type)


# -------------------------------------------------------------------------
# Scheduled tasks
# -------------------------------------------------------------------------
@shared_task(name="task_daily_check_campaigns", ignore_result=True)
def task_daily_check_campaigns():
    """
    This task is executed daily to check the campaigns that have to be sent today. It should be executed at 10:00 AM.
    """
    send_daily_email()


@shared_task(name="task_sync_list_from_acumbamail", ignore_result=True)
def task_sync_list_from_acumbamail():
    """
    This task is executed daily to check the campaigns that have to be sent today. It should be executed at 10:00 AM.
    """
    sync_list_from_acumbamail()


@shared_task(name="example_demo_task", ignore_result=True)
def demo_tasks():
    """
    This function is a demo of how to create a task that is executed every
    """
    print("Hello world")
