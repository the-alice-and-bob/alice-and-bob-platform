"""
This file contains the tasks that are triggered by the EzyCourses webhooks:
"""
from datetime import datetime

from django.conf import settings
from django.db.transaction import atomic

from academy.models import Sells, Student, Product

from celery import shared_task

from campaigns.models import MailList, DailyEmail
from campaigns.sdk import AcumbamailAPI


@shared_task(name="task_campaigns_create_purchase_order", rate_limit="30/m")
def task_create_purchase_order(sell_id: int):
    create_purchase_order(sell_id)


def create_purchase_order(sell_id: int):
    try:
        instance = Sells.objects.get(pk=sell_id)
    except Sells.DoesNotExist:
        raise Exception("Sell not found")

    # Get associated product list
    list_name = instance.product.slug_name

    # Get Product mail list
    try:
        product_mail_list = MailList.objects.get(name=list_name)
    except MailList.DoesNotExist:
        raise Exception("Mail list not found")

    # Get the contact mail list
    try:
        contact_mail_list = MailList.objects.get(name=settings.ACUMBAMAIL_MAIL_LIST_CONTACTS)
    except MailList.DoesNotExist:
        raise Exception("Mail list not found")

    # Get the leads mail list
    try:
        leads_mail_list = MailList.objects.get(name=settings.ACUMBAMAIL_MAIL_LIST_LEADS)
    except MailList.DoesNotExist:
        raise Exception("Mail list not found")

    ac = AcumbamailAPI()

    with atomic():
        # Add to the product list
        # Comprobar si el usuario ya está en la lista de correos
        if not MailList.objects.filter(id=product_mail_list.id, users=instance.student).exists():
            ac.add_subscriber(
                email=instance.student.email,
                name=instance.student.full_name,
                list_id=product_mail_list.acumbamail_id,
            )
            instance.student.mail_lists.add(product_mail_list)

        # If the product price > 0 -> Add to the contact list and remove from leads list
        if instance.sell_price > 0:

            # comprobar si el usuario ya está en la lista de correos
            if not MailList.objects.filter(id=contact_mail_list.id, users=instance.student).exists():

                # Add to the contact list
                ac.add_subscriber(
                    email=instance.student.email,
                    name=instance.student.full_name,
                    list_id=contact_mail_list.acumbamail_id,
                )
                instance.student.mail_lists.add(contact_mail_list)

            # Check if the user is in the leads list
            if Student.objects.filter(mail_lists=leads_mail_list, email=instance.student.email).exists():
                # Delete the user from leads list
                ac.delete_subscriber(
                    email=instance.student.email,
                    list_id=settings.ACUMBAMAIL_MAIL_LIST_LEADS,
                )
                instance.student.mail_lists.remove(leads_mail_list)

        instance.student.save()


@shared_task(name="task_campaigns_create_student", rate_limit="30/m")
def create_student(student_id: int):
    try:
        instance = Student.objects.get(pk=student_id)
    except Student.DoesNotExist:
        raise Exception("Student not found")

    # Get the default mail list
    try:
        default_mail_list = MailList.objects.get(name=settings.ACUMBAMAIL_MAIL_LIST_ALL_USERS)
    except MailList.DoesNotExist:
        raise Exception("Default mail list not found")

    # Get the default mail list
    try:
        leads_mail_list = MailList.objects.get(name=settings.ACUMBAMAIL_MAIL_LIST_LEADS)
    except MailList.DoesNotExist:
        raise Exception("Default mail list not found")

    with atomic():
        ac = AcumbamailAPI()

        # Add the student to the default mail list
        for mail_list in (default_mail_list, leads_mail_list):
            ac.add_subscriber(
                email=instance.email,
                name=instance.full_name,
                list_id=mail_list.acumbamail_id,
            )

            instance.mail_lists.add(mail_list)
            instance.save()


def create_product(product_id: int):
    try:
        instance = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        raise Exception("Product not found")

    AcumbamailAPI().create_mail_list(
        instance.slug_name,
        f'Lista de correo para compradores de {instance.product_name}'
    )


@shared_task(name="task_campaigns_create_product", rate_limit="30/m")
def create_product_task(product_id: int):
    create_product(product_id)


@shared_task(name="task_campaigns_send_email", rate_limit="60/m")
def create_send_campaign_email(daily_email_id: int):
    try:
        instance = DailyEmail.objects.get(pk=daily_email_id)
    except DailyEmail.DoesNotExist:
        raise Exception("Daily Email not found")

    acu = AcumbamailAPI()
    acu.send_many(
        campaign_name=f"[{datetime.today().strftime('%Y-%m-%d')}] {instance.subject}",
        subject=instance.subject,
        body=instance.content,
        scheduled_date=instance.scheduled_at,
        list_id=instance.mail_list.acumbamail_id,
    )
