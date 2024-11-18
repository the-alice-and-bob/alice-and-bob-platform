from datetime import datetime
from typing import Iterable, List
from dataclasses import dataclass, field

from .interfaces import *


class ContactResponseException(Exception):
    ...


class ContactRecordDuplicatedException(Exception):
    ...


@dataclass
class PurchaseOrder:
    subject: str
    ezycourse_id: int
    identifier: int
    contact_name: str
    due_date: datetime
    status: str
    po_date: datetime
    contact_id: int

    def as_zoho(self) -> dict:
        return {
            "Subject": self.subject,
            "id": self.identifier,
            "Contact_Name": self.contact_name,
            "Due_Date": self.due_date.strftime('%Y-%m-%d'),
            "PO_Date": self.po_date.strftime('%Y-%m-%d'),
            "PO_Status": self.status,
            "ID_EzyCourses": self.ezycourse_id,
            "Contact_ID": self.contact_id,
        }

    def add_or_update(self, key, value):
        zoho_map = {
            "id": "identifier",
            "Subject": "subject",
            "Contact_Name": "contact_name",
            "Due_Date": "due_date",
            "PO_Date": "po_date",
            "PO_Status": "status",
            "ID_EzyCourses": "ezycourse_id",
        }

        try:
            setattr(self, zoho_map[key], value)
        except KeyError:
            raise ValueError(f"Invalid key: {key}")


class ZohoPurchaseOrders(Module):
    FIELDS = [
        "Subject",
        "ID_EzyCourse",
        "id",
        "PO_Date",
        "PO_Status",
        "Purchase_Items",
        "Contact_Name"
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def _map_dict(d: dict) -> PurchaseOrder:
        return PurchaseOrder(
            ezycourse_id=d["ID_EzyCourses"],
            identifier=d["id"],
            subject=d["Subject"],
            contact_name=d["Contact_Name"],
            due_date=d["Due_Date"],
            po_date=d["PO_Date"],
            status=d["PO_Status"],
            contact_id=d["Contact_ID"],
        )

    def get_all(self) -> Iterable[PurchaseOrder]:
        for rec in super()._get_records(
                module_name=self.api_name, return_fields=self.FIELDS
        ):
            yield self._map_dict(rec)

    def get_by_email(self, email: str = None) -> PurchaseOrder:
        if found := self._search_by_email(
                email=email,
                module_name=self.api_name, return_fields=self.FIELDS
        ):
            return self._map_dict(found)

    def get_by_id(self, contact_id: int) -> PurchaseOrder:
        if found := self._search_by_id(
                record_id=contact_id,
                module_name=self.api_name, return_fields=self.FIELDS
        ):
            return self._map_dict(found)

    def create(self, contact: PurchaseOrder) -> str | ContactResponseException | ContactRecordDuplicatedException:
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

    def update(self, contact: PurchaseOrder) -> str | ContactResponseException:
        contact_dict = contact.as_zoho()

        try:
            message, data = self._update_record(module_name=self.api_name, record_id=contact.identifier, data=contact_dict)
        except ModuleResponseException as e:
            raise ContactResponseException(e)

        return message


__all__ = ("ZohoPurchaseOrders", "PurchaseOrder")
