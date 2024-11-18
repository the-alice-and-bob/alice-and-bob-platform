from datetime import datetime
from typing import Iterable, List
from dataclasses import dataclass, field

from .interfaces import *


class ContactResponseException(Exception):
    ...


class ContactDuplicatedException(Exception):
    ...


class ContactNotFoundException(Exception):
    ...


FIELD_MAP = {
    "ID_EzyCourses": "ezycourse_id",
    "First_Name": "first_name",
    "Last_Name": "last_name",
    "Email": "email",
    "Phone": "phone",
    "Company": "company",
    "Description": "description",
    "Created_Time": "created_time",
    "Modified_Time": "modified_time",
    "Tag": "tags",
}


@dataclass
class Contact:
    ezycourse_id: int
    identifier: int
    first_name: str
    last_name: str
    email: str
    phone: str
    company: str
    created_time: datetime
    modified_time: datetime
    description: str
    tags: List[Tag] = field(default_factory=list)

    @staticmethod
    def as_zoho() -> dict:
        return FIELD_MAP


class ZohoContacts(BaseModule, ModuleInterface):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_all(self) -> Iterable[Contact]:
        for rec in super()._get_records(
                module_name=self.api_name, return_fields=FIELD_MAP.keys()
        ):
            yield super()._map_zoho_response_with_object(rec, Contact, FIELD_MAP)

    def get_by_email(self, email: str = None) -> Contact | ContactNotFoundException:
        try:
            if found := self._search_by_email(email=email, module_name=self.api_name, return_fields=FIELD_MAP.keys()):
                yield super()._map_zoho_response_with_object(found, Contact, FIELD_MAP)
        except ModuleException as e:
            raise ContactNotFoundException(e)

    def get_by_id(self, contact_id: int) -> Contact | ContactNotFoundException:
        try:
            if found := self._search_by_id(record_id=contact_id, module_name=self.api_name, return_fields=FIELD_MAP.keys()):
                return super()._map_zoho_response_with_object(found, Contact, FIELD_MAP)
        except ModuleException as e:
            raise ContactNotFoundException(e)

    def create(self, contact: Contact) -> bool | ContactResponseException | ContactDuplicatedException:
        contact_dict = Contact.as_zoho()

        try:
            self._create_record(module_name=self.api_name, data=contact_dict)
        except ModuleRecordDuplicatedException as e:
            raise ContactDuplicatedException(e)

        except ModuleException as e:
            raise ContactResponseException(e)

        return True

    def update(self, record_id: int, **kwargs) -> bool | ContactResponseException | ContactNotFoundException:
        contact_dict = Contact.as_zoho()

        try:
            self._update_record(module_name=self.api_name, record_id=record_id, data=contact_dict)
        except ModuleRecordDuplicatedException as e:
            raise ContactNotFoundException(e)

        except ModuleException as e:
            raise ContactResponseException(e)

        return True

    def delete(self, record_id: int) -> bool | ContactNotFoundException:
        try:
            self._delete_record(module_name=self.api_name, record_id=record_id)
        except ModuleRecordNotFound:
            raise ContactNotFoundException(f"Lead with id {record_id} not found")

        return True


__all__ = ("ZohoContacts", "Contact")
