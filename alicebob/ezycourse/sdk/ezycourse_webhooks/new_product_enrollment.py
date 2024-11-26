from django.db.transaction import atomic

from academy.models import Product, Sells

from .helpers import *
from .models import NewProduct


def ezycourse_new_product_enrollment(data: dict):
    """
    This webhook is triggered when a new user signs up.
    """
    try:
        obj = NewProduct.from_json(data)
    except Exception as e:
        raise ValueError(f"Invalid data: {e}")

    student = get_or_create_student(obj)

    # Now we have to get the product ID
    with atomic():

        # Get course db object
        try:
            course = Product.objects.get(ezy_id=obj.product_id)
        except Product.DoesNotExist:
            print(f"Course {obj.product_id} not found in the DB")
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

        # Add tags to the student
        student.tags.add(*course.tags.all())

        print(f"Student {student} enrolled in course {course}")

__all__ = ("ezycourse_new_product_enrollment",)
