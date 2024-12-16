import logging

from django.db.transaction import atomic

from academy.models import Product, Sells

from .helpers import *
from .models import NewProduct

db_logger = logging.getLogger("db")


def ezycourse_new_product_enrollment(data: dict):
    """
    This webhook is triggered when a new user signs up.
    """
    try:
        obj = NewProduct.from_json(data)
    except Exception as e:
        db_logger.error(f"Invalid data while processing new product enrollment: {e}")
        return

    student = get_or_create_student(obj)

    # Now we have to get the product ID
    with atomic():

        # Get course db object
        try:
            course = Product.objects.get(ezy_id=obj.product_id)
        except Product.DoesNotExist:
            db_logger.error(f"Course {obj.product_id} not found in the DB while processing new sale")
            return

        try:
            Sells.objects.get(student=student, product=course)
        except Sells.DoesNotExist:
            Sells.objects.create(
                student=student,
                product=course,
                subject=course.product_name,
                gateway=obj.gateway,
                sell_price=0,
            )

        db_logger.info(f"Student {student} enrolled in course {course}")


__all__ = ("ezycourse_new_product_enrollment",)
