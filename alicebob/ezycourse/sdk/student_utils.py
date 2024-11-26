from typing import Iterable

from awesome_ezycourse.sdk import Courses, Users, UserEnrollmentStatus
from academy.models import ProductTypes, Product, Student

from ..sdk import ezycourse_instance


def check_and_update_student_progress():
    """
    This task updates the student progress.
    """
    auth = ezycourse_instance()

    print(f"Listing EzyCourse courses...")

    ezy_courses = Courses(auth=auth)

    # Get all the DB courses
    db_courses_ids = Product.objects.filter(product_type=ProductTypes.COURSE).values_list('ezy_id', flat=True)

    for course_id in db_courses_ids:
        course = ezy_courses.get(course_id)

        for student in course.get_enrolled():
            ...


def populate_students() -> Iterable[Student]:
    """
    Populate the DB with Ezycourse students
    """
    auth = ezycourse_instance()

    print(f"Listing EzyCourse courses...")

    for user in Users(auth=auth).get_users(only_students=True, enrollment_status=UserEnrollmentStatus.ALL):
        try:
            student = Student.objects.get(email=user.email)
            already_exists = True
        except Student.DoesNotExist:
            already_exists = False
            student = Student.objects.create(
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                ezy_id=user.identifier,
                name=user.full_name,
                created_date=user.created_at,
                last_login=user.last_login,
            )

        if already_exists:
            continue

        yield student
