from typing import Iterable

from awesome_ezycourse.sdk import Courses, CourseStatus
from academy.models import Product, ProductTypes

from .auth import ezycourse_instance


def populate_courses() -> Iterable[Product]:

    courses = Courses(auth=ezycourse_instance())

    for course, course_statistics in courses.list_courses():

        if course.is_published != CourseStatus.PUBLISHED:
            continue

        # Get extra details for the course
        course_details = courses.get(course.identifier)

        try:
            product = Product.objects.get(ezy_id=course.identifier)
            already_exists = True
        except Product.DoesNotExist:
            already_exists = False
            product = Product.objects.create(
                ezy_id=course.identifier,
                product_type=ProductTypes.COURSE,
                product_name=course.title,
                price=course_details.price,
                description=course.short_description,
                language=course.language,
                image=course.image,
                published_date=course.published_date,
            )

        if already_exists:
            continue

        yield product


__all__ = ('populate_courses',)
