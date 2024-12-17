"""
This file contains the tasks that are triggered by the EzyCourses webhooks:
"""
from celery import shared_task

from .engine import *


# -------------------------------------------------------------------------
# Tasks for the Acumbamail list management
# -------------------------------------------------------------------------
@shared_task(name="task_create_purchase_order", rate_limit="30/m")
def task_create_purchase_order(sell_id: int):
    """
    This task creates a purchase order in Acumbamail
    """
    create_purchase_order(sell_id)


@shared_task(name="task_create_student", rate_limit="30/m")
def task_create_student(student_id: int):
    create_student(student_id)


@shared_task(name="task_create_product", rate_limit="30/m")
def task_create_product(product_id: int):
    create_product(product_id)


@shared_task(name="task_create_send_campaign_email", rate_limit="60/m")
def task_create_send_campaign_email(daily_email_id: int):
    create_send_campaign_email(daily_email_id)


# -------------------------------------------------------------------------
# End of tasks for the Acumbamail list management
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# Tasks for webhooks
# -------------------------------------------------------------------------
@shared_task(name="task_process_acumbamail_webhook")
def task_process_acumbamail_webhook(list_id, email, timestamp, event_type):
    handle_action(list_id, email, timestamp, event_type)
