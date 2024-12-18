from academy.models import Student

from .models import LessonCompleted, ChapterCompleted, CourseCompleted, NewProduct, NewSignup


class UserCreationException(Exception):
    ...


def get_or_create_student(obj: NewProduct | NewSignup | LessonCompleted | ChapterCompleted | CourseCompleted) -> Student:
    # Check if the user already exists
    try:
        return Student.objects.get(ezy_id=obj.identifier)
    except Student.DoesNotExist:
        return Student.objects.create(
            ezy_id=obj.identifier,
            email=obj.email,
            first_name=obj.first_name,
            last_name=obj.last_name,
        )


__all__ = ("get_or_create_student",)
