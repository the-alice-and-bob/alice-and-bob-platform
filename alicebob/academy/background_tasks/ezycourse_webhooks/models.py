from enum import Enum

from dataclasses import dataclass


class ProductTypes(Enum):
    COURSE = 'course'
    BUNDLE_COURSE = 'bundle_course'
    PRIVATE_CHAT = 'private_chat'
    COMMUNITY = 'community'
    GROUP = 'group'
    DIGITAL_PRODUCT = 'digital_product'
    PHYSICAL_PRODUCT = 'physical_product'
    VIDEO_LIBRARY = 'video_library'
    MEMBERSHIP = 'membership'
    ORGANIZATION = 'organization'


@dataclass
class NewSignup:
    """
    id	Id of the student.
    first_name	First name of the student.
    last_name	Last name of the student.
    name	Name of the student. Value should be 3 to 50 characters long.
    email	Email of the student. Value should be 50 characters long.
    """
    identifier: int
    first_name: str
    last_name: str
    name: str
    email: str

    @classmethod
    def from_json(cls, data: dict) -> 'NewSignup':
        return cls(
            identifier=data.get('id'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            name=data.get('name'),
            email=data.get('email')
        )


@dataclass
class NewProduct:
    """
    id	Id of the student.
    first_name	First name of the student.
    last_name	Last name of the student.
    name	Name of the student. Value should be 3 to 50 characters long.
    email	Email of the student. Value should be 50 characters long.
    product_id	Product id will be the id of the product. Value will be integer. This is required when product_type is not 'private_chat'.
    product_type	Product type will be one of the following: 'course', 'bundle_course', 'private_chat', 'community', 'group', 'digital_product', 'physical_product', 'video_library', 'membership','organization'.
    product_name	Name of the product
    price	Price of the sold product.
    gateway	Payment gateway of the sold product.
    """
    identifier: int  # EzyCourse ID
    first_name: str
    last_name: str
    name: str
    email: str
    product_id: int
    product_type: ProductTypes
    product_name: str
    price: float
    gateway: str

    @classmethod
    def from_json(cls, data: dict) -> 'NewProduct':
        return cls(
            identifier=data.get('id'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            name=data.get('name'),
            email=data.get('email'),
            product_id=data.get('product_id'),
            product_type=ProductTypes(data.get('product_type')),
            product_name=data.get('product_name'),
            price=data.get('price'),
            gateway=data.get('gateway')
        )


@dataclass
class CourseCompleted:
    """
    id	Id of the student.
    first_name	First name of the student.
    last_name	Last name of the student.
    name	Name of the student. Value should be 3 to 50 characters long.
    email	Email of the student. Value should be 50 characters long.
    course_id	Id of the completed course.
    course_name	Name of the completed course.
    """
    identifier: int
    first_name: str
    last_name: str
    name: str
    email: str
    course_id: int
    course_name: str

    @classmethod
    def from_json(cls, data: dict) -> 'CourseCompleted':
        return cls(
            identifier=data.get('id'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            name=data.get('name'),
            email=data.get('email'),
            course_id=data.get('course_id'),
            course_name=data.get('course_name')
        )


@dataclass
class ChapterCompleted:
    """
    id	Id of the student.
    first_name	First name of the student.
    last_name	Last name of the student.
    name	Name of the student. Value should be 3 to 50 characters long.
    email	Email of the student. Value should be 50 characters long.
    course_id	Id of the completed course.
    course_name	Name of the completed course.
    chapter_id	Id ofs the completed chapter.
    chapter_name	Name of the completed chapter.
    """
    identifier: int
    first_name: str
    last_name: str
    name: str
    email: str
    course_id: int
    course_name: str
    chapter_id: int
    chapter_name: str

    @classmethod
    def from_json(cls, data: dict) -> 'ChapterCompeleted':
        return cls(
            identifier=data.get('id'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            name=data.get('name'),
            email=data.get('email'),
            course_id=data.get('course_id'),
            course_name=data.get('course_name'),
            chapter_id=data.get('chapter_id'),
            chapter_name=data.get('chapter_name')
        )


@dataclass
class QuizCompleted:
    """
    id	Id of the student.
    first_name	First name of the student.
    last_name	Last name of the student.
    name	Name of the student. Value should be 3 to 50 characters long.
    course_name	Name of the completed course.
    chapter_id	Id of the completed chapter.
    chapter_name	Name of the completed chapter.
    lesson_id	Id of the completed lesson.
    lesson_name	Name of the completed lesson.
    how_many_qu	Number of the questions
    correct_answer	Number of the correct answer
    total_mark	Total marks
    date	Submitted date
    wrong_answer	Number of wrong answer
    """
    identifier: int
    first_name: str
    last_name: str
    name: str
    course_name: str
    chapter_id: int
    chapter_name: str
    lesson_id: int
    lesson_name: str
    how_many_qu: int
    correct_answer: int
    total_mark: int
    date: str
    wrong_answer: int

    @classmethod
    def from_json(cls, data: dict) -> 'QuizCompleted':
        return cls(
            identifier=data.get('id'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            name=data.get('name'),
            course_name=data.get('course_name'),
            chapter_id=data.get('chapter_id'),
            chapter_name=data.get('chapter_name'),
            lesson_id=data.get('lesson_id'),
            lesson_name=data.get('lesson_name'),
            how_many_qu=data.get('how_many_qu'),
            correct_answer=data.get('correct_answer'),
            total_mark=data.get('total_mark'),
            date=data.get('date'),
            wrong_answer=data.get('wrong_answer')
        )


@dataclass
class LessonCompleted:
    """
    id	Id of the student.
    first_name	First name of the student.
    last_name	Last name of the student.
    name	Name of the student. Value should be 3 to 50 characters long.
    email	Email of the student. Value should be 50 characters long.
    course_id	Id of the completed course.
    course_name	Name of the completed course.
    chapter_id	Id of the completed chapter.
    chapter_name	Name of the completed chapter.
    lesson_id	Id of the completed lesson.
    lesson_name	Name of the completed lesson.
    date	Submitted date
    """
    identifier: int
    first_name: str
    last_name: str
    name: str
    email: str
    course_id: int
    course_name: str
    chapter_id: int
    chapter_name: str
    lesson_id: int
    lesson_name: str
    date: str

    @classmethod
    def from_json(cls, data: dict) -> 'LessonCompleted':
        return cls(
            identifier=data.get('id'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            name=data.get('name'),
            email=data.get('email'),
            course_id=data.get('course_id'),
            course_name=data.get('course_name'),
            chapter_id=data.get('chapter_id'),
            chapter_name=data.get('chapter_name'),
            lesson_id=data.get('lesson_id'),
            lesson_name=data.get('lesson_name'),
            date=data.get('date')
        )


__all__ = ("NewSignup", "NewProduct", "CourseCompleted", "ChapterCompleted", "QuizCompleted", "LessonCompleted")
