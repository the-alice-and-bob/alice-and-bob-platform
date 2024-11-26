from django.conf import settings
from django.db.transaction import atomic
from django.dispatch import receiver
from django.db.models.signals import post_save

from celery_app import app as background_task
from academy.models import Product, Student, Sells, CourseProgress, Tag

from .models import ZohoProduct, ZohoCourseProgress, ZohoTag, ZohoContact, ZohoPurchaseOrders, ZohoLead


@receiver(post_save, sender=Tag)
def create_tag(sender, instance, **kwargs):
    try:
        zoho_tag = ZohoTag.objects.get(tag=instance)
    except ZohoTag.DoesNotExist:
        zoho_tag = ZohoTag.objects.create(tag=instance)

    if settings.ZOHO_ENABLE_SYNC:
        # Sync with Zoho
        background_task.send_task("task_zoho_create_tag", args=(zoho_tag.id,))


@receiver(post_save, sender=Product)
def create_product(sender, instance, **kwargs):
    try:
        zoho_product = ZohoProduct.objects.get(product=instance)
    except ZohoProduct.DoesNotExist:
        zoho_product = ZohoProduct.objects.create(product=instance)

    if settings.ZOHO_ENABLE_SYNC:
        # Sync with Zoho
        background_task.send_task("task_zoho_create_product", args=(zoho_product.id,))


@receiver(post_save, sender=Student)
def create_student(sender, instance, **kwargs):
    try:
        zoho_lead = ZohoLead.objects.get(student=instance)
    except ZohoLead.DoesNotExist:
        zoho_lead = ZohoLead.objects.create(student=instance)

    if settings.ZOHO_ENABLE_SYNC:
        # Sync with Zoho
        background_task.send_task("task_zoho_create_lead", args=(zoho_lead.id,))


@receiver(post_save, sender=CourseProgress)
def create_course_progress(sender, instance, **kwargs):
    try:
        zoho_course_progress = ZohoCourseProgress.objects.get(
            student=instance.student,
            product=instance.course,
            course_progress=instance
        )

    except ZohoCourseProgress.DoesNotExist:
        zoho_course_progress = ZohoCourseProgress.objects.create(
            student=instance.student,
            product=instance.course,
            course_progress=instance
        )

    if settings.ZOHO_ENABLE_SYNC:
        # Sync with Zoho
        background_task.send_task("task_zoho_create_course_progress", args=(zoho_course_progress.id,))


@receiver(post_save, sender=Sells)
def create_purchase_order(sender, instance, **kwargs):

    with atomic():

        try:
            zoho_purchase_order = ZohoPurchaseOrders.objects.get(
                student=instance.student,
                product=instance.product,
                sell=instance,
            )
        except ZohoPurchaseOrders.DoesNotExist:
            zoho_purchase_order = ZohoPurchaseOrders.objects.create(
                student=instance.student,
                product=instance.product,
                sell=instance,
            )

        # Create a new Zoho Contact and remove the Lead
        try:
            ZohoContact.objects.get(student=instance.student)
        except ZohoContact.DoesNotExist:
            ZohoContact.objects.create(student=instance.student)

        try:
            zoho_lead = ZohoLead.objects.get(student=instance.student)
            zoho_lead.delete()
        except ZohoLead.DoesNotExist:
            pass

        if settings.ZOHO_ENABLE_SYNC:
            # Sync with Zoho
            background_task.send_task("task_zoho_create_purchase_order", args=(zoho_purchase_order.id,))
