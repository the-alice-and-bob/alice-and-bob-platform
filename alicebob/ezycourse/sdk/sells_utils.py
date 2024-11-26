from typing import Iterable, Tuple

from django.db.transaction import atomic

from awesome_ezycourse.sdk import Courses
from academy.models import Product, Student, Sells, CourseProgress

from ..sdk import ezycourse_instance


def populate_sells() -> Iterable[Tuple[Student, Product]]:
    """
    Populate the DB with Ezycourse students
    """
    auth = ezycourse_instance()

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
                    Sells.objects.create(
                        student=student,
                        product=course,
                        subject=course.product_name,
                        gateway=enrollment.gateway,
                        sell_price=course.price,
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

                # Update Student tags
                student.tags.add(*course.tags.all())

                yield student, course


__all__ = ('populate_sells',)
