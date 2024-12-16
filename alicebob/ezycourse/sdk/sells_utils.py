from typing import Iterable, Tuple

from django.db.transaction import atomic

from awesome_ezycourse.sdk import Courses, Communities
from academy.models import Product, Student, Sells, CourseProgress

from ..sdk import ezycourse_instance


def populate_sells() -> Iterable[Tuple[Student, Product]]:
    """
    Populate the DB with Ezycourse students
    """
    auth = ezycourse_instance()

    # -------------------------------------------------------------------------
    # Now we need to get the list of communities
    # -------------------------------------------------------------------------
    for community in Communities(auth).list():

        # Get community db object
        try:
            product = Product.objects.get(ezy_id=community.identifier)
        except Product.DoesNotExist:
            print(f"Community {community.identifier} not found in the DB")
            continue

        # Get enrolled students
        for member in community.list_members():

            with atomic():

                # Get the student
                try:
                    student = Student.objects.get(ezy_id=member.identifier)
                except Student.DoesNotExist:
                    print(f"Student {member.identifier} not found in the DB from community {community.identifier} or is an admin")
                    continue

                try:
                    Sells.objects.get(student=student, product=product)
                except Sells.DoesNotExist:
                    Sells.objects.create(
                        student=student,
                        product=product,
                        subject=product.product_name,
                        sell_price=product.price,
                        date=member.last_login
                    )

                yield student, product

    # -------------------------------------------------------------------------
    # First we need to get the list of courses
    # -------------------------------------------------------------------------
    for ezy_course, _ in Courses(auth).list_courses():

        # Get course db object
        try:
            course = Product.objects.get(ezy_id=ezy_course.identifier)
        except Product.DoesNotExist:
            print(f"Course {ezy_course.identifier} not found in the DB")
            continue

        # Get enrolled students
        for enrollment in ezy_course.get_enrolled():

            with atomic():

                # Get the student
                try:
                    student = Student.objects.get(email=enrollment.student.email)
                except Student.DoesNotExist:
                    print(f"Student {enrollment.student.email} not found in the DB")
                    continue

                try:
                    Sells.objects.get(student=student, product=course)
                except Sells.DoesNotExist:
                    if enrollment.user_paid_course:
                        sell_price = course.price
                    else:
                        sell_price = 0

                    Sells.objects.create(
                        student=student,
                        product=course,
                        subject=course.product_name,
                        gateway=enrollment.gateway,
                        sell_price=sell_price,
                        date=enrollment.created,
                    )

                try:
                    course_progress = CourseProgress.objects.get(student=student, course=course)
                except CourseProgress.DoesNotExist:
                    course_progress = CourseProgress.objects.create(
                        student=student,
                        course=course,
                        progress=enrollment.progress
                    )

                updated = False
                if enrollment.progress > course_progress.progress:
                    updated = True
                    course_progress.progress = enrollment.progress

                if enrollment.course_completion_date and not course_progress.completed_date:
                    updated = True
                    course_progress.completed_date = enrollment.course_completion_date

                if course_progress.completed_date and course_progress.progress < 100:
                    updated = True
                    course_progress.progress = 100

                if updated:
                    course_progress.save()

                yield student, course


__all__ = ('populate_sells',)
