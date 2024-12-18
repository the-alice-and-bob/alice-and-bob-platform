from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save

from campaigns.models import EmailCampaigns
from academy.models import Product, Student, Sells

from celery_app import app as background_task

from .tasks import create_purchase_order, create_product, create_send_campaign_email, create_student


# @receiver(post_save, sender=EmailCampaigns)
# def signal_send_email(sender, instance, created, **kwargs):
#     if created:
#         if settings.DEBUG:
#             create_send_campaign_email(instance.id)
#         else:
#             background_task.send_task("task_create_send_campaign_email", args=(instance.id,))


@receiver(post_save, sender=Product)
def signal_create_product(sender, instance, created, **kwargs):
    # Each product has its own mail list
    if created:
        if settings.DEBUG:
            create_product(instance.id)
        else:
            background_task.send_task("task_create_product", args=(instance.id,))


@receiver(post_save, sender=Student)
def signal_create_student(sender, instance, created, **kwargs):
    # Add the student to the default mail list

    if created:
        if settings.DEBUG:
            create_student(instance.id)
        else:
            background_task.send_task("task_create_student", args=(instance.id,))


@receiver(post_save, sender=Sells)
def signal_create_purchase_order(sender, instance, created, **kwargs):

    if created:
        if settings.DEBUG:
            create_purchase_order(instance.id)
        else:
            background_task.send_task("task_create_purchase_order", args=(instance.id,))
