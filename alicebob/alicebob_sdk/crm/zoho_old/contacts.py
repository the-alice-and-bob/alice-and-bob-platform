from datetime import datetime
from typing import Iterable, List
from dataclasses import dataclass, field

from .interfaces import *


class ContactResponseException(Exception):
    ...


class ContactRecordDuplicatedException(Exception):
    ...


@dataclass
class Tag:
    identifier: int
    name: str


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

    def as_zoho(self) -> dict:
        return {
            "ID_EzyCourses": self.ezycourse_id,
            "First_Name": self.first_name,
            "Last_Name": self.last_name,
            "Email": self.email,
            "Phone": self.phone,
            "Company": self.company,
            "Description": self.description,
            "Created_Time": self.created_time,
            "Modified_Time": self.modified_time,
            "Tag": self.tags,
        }

    def add_or_update(self, key, value):
        zoho_map = {
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

        if key == "Tag":
            self.tags = [Tag(identifier=tag["id"], name=tag["name"]) for tag in value]

        else:
            try:
                setattr(self, zoho_map[key], value)
            except KeyError:
                raise ValueError(f"Invalid key: {key}")


class ZohoContacts(Module):
    FIELDS = [
        "id", "ID_EzyCourses", "First_Name", "Last_Name", "Email", "Phone", "Company", "Created_Time", "Modified_Time",
        "Description", "Website", "Tag"
    ]
    properties_map = {
        "ID_EzyCourse": "ID_EzyCourses",
        "ezy_course_id": "ID_EzyCourses",
        "ezycourse_id": "ID_EzyCourses",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def _map_dict(d: dict) -> Contact:

        return Contact(
            ezycourse_id=d["ID_EzyCourses"],
            identifier=d["id"],
            first_name=d["First_Name"],
            last_name=d["Last_Name"],
            email=d["Email"],
            phone=d["Phone"],
            company=d["Company"],
            created_time=d["Created_Time"],
            modified_time=d["Modified_Time"],
            description=d["Description"],
            tags=[Tag(identifier=tag["id"], name=tag["name"]) for tag in super()._parse_tags(d)]
        )

    def get_all(self) -> Iterable[Contact]:
        for rec in super()._get_records(
                module_name=self.api_name, return_fields=self.FIELDS
        ):
            yield self._map_dict(rec)

    def get_by_email(self, email: str = None) -> Contact:
        if found := self._search_by_email(
                email=email,
                module_name=self.api_name, return_fields=self.FIELDS
        ):
            return self._map_dict(found)

    def get_by_id(self, contact_id: int) -> Contact:
        if found := self._search_by_id(
                record_id=contact_id,
                module_name=self.api_name, return_fields=self.FIELDS
        ):
            return self._map_dict(found)

    def create(self, contact: Contact) -> str | ContactResponseException | ContactRecordDuplicatedException:
        contact_dict = contact.as_zoho()

        try:
            message, data = self._create_record(module_name=self.api_name, data=contact_dict)
        except ModuleRecordDuplicatedException as e:
            raise ContactRecordDuplicatedException(e)

        except ModuleResponseException as e:
            raise ContactResponseException(e)

        # Update the lead structure with the new data
        for k, v in data.items():
            contact.add_or_update(k, v)

        return message

    def update(self, contact: Contact) -> str | ContactResponseException:
        contact_dict = contact.as_zoho()

        try:
            message, data = self._update_record(module_name=self.api_name, record_id=contact.identifier, data=contact_dict)
        except ModuleResponseException as e:
            raise ContactResponseException(e)

        return message


__all__ = ("ZohoContacts", "Contact")
