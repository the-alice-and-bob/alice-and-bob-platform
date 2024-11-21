from datetime import datetime
from typing import Iterable, List, Optional
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
    identifier: int


@dataclass
class CourseBrief:
    name: str
    identifier: int


@dataclass
class CourseProgress(RecordInterface):
    course: CourseBrief
    customer: Buyer
    progress: int = 0

    current_chapter: Optional[str] = None
    current_lesson: Optional[str] = None
    start_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None
    last_visit: Optional[datetime] = None
    identifier: Optional[int] = None

    @property
    def zoho_map(self) -> dict:
        return FIELD_MAP

    def __post_init__(self):
        if isinstance(self.customer, dict):
            self.customer = Buyer(name=self.customer.get("name"), identifier=self.customer.get("identifier"))

        if isinstance(self.course, dict):
            self.course = CourseBrief(name=self.course.get("name"), identifier=self.course.get("identifier"))


class ZohoCourseProgress(BaseModule, ModuleInterface):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _custom_to_zoho_serializer(self, data: CourseProgress) -> dict:
        return {
            "id": data.identifier,
            "Course": {
                "name": data.course.name,
                "id": data.course.identifier
            },
            "Customer": {
                "name": data.customer.name,
                "id": data.customer.identifier
            },
            "Progress": data.progress,
            "Current_Chapter": data.current_chapter,
            "Current_Lesson": data.current_lesson,
            "Start_Date": data.start_date,
            "Completed_Date": data.completed_date,
            "Last_Visit": data.last_visit,
        }

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
            ("Customer.id", "equals", customer),
            ("Course.id", "equals", course)
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

    def create(self, course_progress: CourseProgress) -> int | CourseProgressResponseException | CourseProgressDuplicatedException:
        course_progress_dict = self._custom_to_zoho_serializer(course_progress)

        try:
            return self._create_record(module_name=self.api_name, data=course_progress_dict)
        except ModuleRecordDuplicatedException as e:
            raise CourseProgressDuplicatedException(e)

        except ModuleException as e:
            raise CourseProgressResponseException(e)

    def update(self, record_id: int, **kwargs) -> bool | CourseProgressResponseException | CourseProgressNotFoundException:

        # TODO: HAY QUE HACER EL MAPEO PERDIDO. HACIENDO QUE EL KWARGS CORRESPONDA CON LA PROPIEDAD ADECUADA ZOHO
        # Esto funciona:     course_progress.update(record_id=cp.identifier, Progress=100)
        # Esto no:     course_progress.update(record_id=cp.identifier, progress=100)
        course_progress = CourseProgress.from_object(FIELD_MAP, kwargs)

        try:
            self._update_record(module_name=self.api_name, record_id=record_id, data=course_progress)
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


__all__ = (
    "ZohoCourseProgress", "CourseProgress", "CourseProgressNotFoundException", "CourseProgressResponseException",
    "CourseProgressDuplicatedException", "Buyer", "CourseBrief"
)
