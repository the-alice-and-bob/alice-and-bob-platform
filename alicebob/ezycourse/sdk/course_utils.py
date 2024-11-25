from typing import Iterable

from awesome_ezycourse.sdk import Courses, CourseStatus
from academy.models import Product, ProductTypes

from .auth import ezycourse_instance


def populate_courses() -> Iterable[Product]:

    courses = Courses(auth=ezycourse_instance())

    for course, course_statistics in courses.list_courses():

        # Get extra details for the course
        course_details = courses.get(course.identifier)

        # Check if the course already exists in the database, otherwise create it
        product, created = Product.objects.get_or_create(
            ezy_id=course.identifier,
            product_type=ProductTypes.COURSE,
            product_name=course.title,
            price=course_details.price,
            description=course.short_description,
            language=course.language,
            image=course.image,
            published_date=course.published_date,
        )

        if created:
            yield product


__all__ = ('populate_courses',)
