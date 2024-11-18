from datetime import datetime
from typing import Iterable, List
from dataclasses import dataclass, field

from .interfaces import *
from .contacts import Contact


class CourseProgressResponseException(Exception):
    ...


class CourseProgressDuplicatedException(Exception):
    ...


class CourseProgressNotFoundException(Exception):
    ...


FIELD_MAP = {
    "id": "identifier",
    "Course": "course",
    "Customer": "customer",
    "Progress": "progress",
    "Current_Chapter": "current_chapter",
    "Current_Lesson": "current_lesson",
    "Start_Date": "start_date",
    "Completed_Date": "completed_date",
    "Last_Visit": "last_visit",
}


@dataclass
class Buyer:
    name: str
    identifier: str


@dataclass
class CourseBrief:
    name: str
    identifier: str


@dataclass
class CourseProgress:
    identifier: int
    course: CourseBrief
    customer: Buyer
    progress: int
    current_chapter: str
    current_lesson: str
    start_date: datetime
    completed_date: datetime
    last_visit: datetime

    @staticmethod
    def as_zoho() -> dict:
        return FIELD_MAP

    def __post_init__(self):
        if isinstance(self.customer, dict):
            self.customer = Buyer(name=self.customer.get("name"), identifier=self.customer.get("identifier"))

        if isinstance(self.course, dict):
            self.course = CourseBrief(name=self.course.get("name"), identifier=self.course.get("identifier"))


class ZohoCourseProgress(BaseModule, ModuleInterface):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_all(self) -> Iterable[CourseProgress]:
        for rec in super()._get_records(
                module_name=self.api_name, return_fields=FIELD_MAP.keys()
        ):
            yield super()._map_zoho_response_with_object(rec, CourseProgress, FIELD_MAP)

    def get_by_customer_and_course(self, customer: int | Contact, course: int | CourseBrief) -> CourseProgress | CourseProgressNotFoundException:
        if isinstance(customer, Contact):
            customer = customer.identifier

        if isinstance(course, CourseBrief):
            course = course.identifier

        criteria = [
            ("Customer", "equals", customer),
            ("Course", "equals", course)
        ]

        try:
            if found := self._search_by_field(criteria=criteria, module_name=self.api_name, return_fields=FIELD_MAP.keys()):
                return super()._map_zoho_response_with_object(found, CourseProgress, FIELD_MAP)
        except ModuleException as e:
            raise CourseProgressNotFoundException(e)

    def get_by_id(self, record_id: int) -> CourseProgress | CourseProgressNotFoundException:
        try:
            if found := self._search_by_id(record_id=record_id, module_name=self.api_name, return_fields=FIELD_MAP.keys()):
                return super()._map_zoho_response_with_object(found, CourseProgress, FIELD_MAP)
        except ModuleException as e:
            raise CourseProgressNotFoundException(e)

    def create(self, course_progress: CourseProgress) -> bool | CourseProgressResponseException | CourseProgressDuplicatedException:
        course_progress_dict = CourseProgress.as_zoho()

        try:
            self._create_record(module_name=self.api_name, data=course_progress_dict)
        except ModuleRecordDuplicatedException as e:
            raise CourseProgressDuplicatedException(e)

        except ModuleException as e:
            raise CourseProgressResponseException(e)

        return True

    def update(self, record_id: int, **kwargs) -> bool | CourseProgressResponseException | CourseProgressNotFoundException:

        # TODO: HAY QUE HACER EL MAPEO PERDIDO. HACIENDO QUE EL KWARGS CORRESPONDA CON LA PROPIEDAD ADECUADA ZOHO
        # Esto funciona:     course_progress.update(record_id=cp.identifier, Progress=100)
        # Esto no:     course_progress.update(record_id=cp.identifier, progress=100)

        try:
            self._update_record(module_name=self.api_name, record_id=record_id, data=kwargs)
        except ModuleRecordDuplicatedException as e:
            raise CourseProgressNotFoundException(e)

        except ModuleException as e:
            raise CourseProgressResponseException(e)

        return True

    def delete(self, record_id: int) -> bool | CourseProgressNotFoundException:
        try:
            self._delete_record(module_name=self.api_name, record_id=record_id)
        except ModuleRecordNotFound:
            raise CourseProgressNotFoundException(f"Course progress with id {record_id} not found")

        return True


__all__ = ("ZohoCourseProgress", "CourseProgress")
