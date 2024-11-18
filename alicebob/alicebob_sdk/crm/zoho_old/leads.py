from datetime import datetime
from typing import Iterable, List
from dataclasses import dataclass, field

from zohocrmsdk.src.com.zoho.crm.api.record import GetRecordsParam

from .interfaces import *


class LeadResponseException(Exception):
    ...


class LeadRecordDuplicatedException(Exception):
    ...


@dataclass
class Tag:
    identifier: int
    name: str


@dataclass
class Lead:
    email: str
    last_name: str
    ezycourse_id: int = None
    identifier: int = None
    first_name: str = None
    phone: str = None
    company: str = None
    created_time: datetime = None
    modified_time: datetime = None
    description: str = None
    website: str = None
    lead_source: str = None
    owner: str = None
    tags: List[Tag] = field(default_factory=list)

    def as_zoho(self) -> dict:
        return {
            "ID_EzyCourse": self.ezycourse_id,
            "First_Name": self.first_name,
            "Last_Name": self.last_name,
            "Email": self.email,
            "Phone": self.phone,
            "Company": self.company,
            "Description": self.description,
            "Website": self.website,
            "Lead_Source": self.lead_source,
            "Tag": self.tags,
        }

    def add_or_update(self, key, value):
        zoho_map = {
            "ID_EzyCourse": "ezycourse_id",
            "First_Name": "first_name",
            "Last_Name": "last_name",
            "Email": "email",
            "Phone": "phone",
            "Company": "company",
            "Description": "description",
            "Website": "website",
            "Lead_Source": "lead_source",
            "Tag": "tags",
        }

        if key == "Tag":
            self.tags = [Tag(identifier=tag["id"], name=tag["name"]) for tag in value]
        else:
            try:
                setattr(self, zoho_map[key], value)
            except KeyError:
                raise ValueError(f"Invalid key: {key}")


class ZohoLeads(Module):
    LEAD_FIELDS = [
        "id", "ID_EzyCourse", "Lead_Status", "First_Name", "Last Name", "Email", "Phone", "Company", "Created_Time", "Modified _Time",
        "Description", "Website", "Lead_Name", "Lead_Source", "Tag"
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def _map_dict(d: dict) -> Lead:
        lead_source = d.get("Lead_Source").get_value() if d.get("Lead_Source", None) else None

        return Lead(
            ezycourse_id=d.get("ID_EzyCourse"),
            identifier=d.get("id"),
            first_name=d.get("First_Name"),
            last_name=d.get("Last_Name"),
            email=d.get("Email"),
            phone=d.get("Phone"),
            company=d.get("Company"),
            created_time=d.get("Created_Time"),
            modified_time=d.get("Modified_Time"),
            description=d.get("Description"),
            website=d.get("Website"),
            lead_source=lead_source,
            tags=[Tag(identifier=tag["id"], name=tag["name"]) for tag in super()._parse_tags(d)]
        )

    def get_all(self) -> Iterable[Lead]:
        records = [
            (GetRecordsParam.approved, "true"),
            (GetRecordsParam.converted, "false"),
        ]

        for lead in super()._get_records(
                module_name=self.api_name, return_fields=self.LEAD_FIELDS,
                additional_record_operations=records
        ):
            yield self._map_dict(lead)

    def get_lead(self, lead_id: int):
        pass

    def get_by_email(self, email: str) -> Lead:
        if found := self._search_by_email(
                email=email,
                module_name=self.api_name, return_fields=self.LEAD_FIELDS
        ):
            return self._map_dict(found)

    def get_by_id(self, lead_id: int) -> Lead:
        if found := self._search_by_id(
                record_id=lead_id,
                module_name=self.api_name, return_fields=self.LEAD_FIELDS
        ):
            return self._map_dict(found)

    def create(self, lead: Lead) -> str | LeadRecordDuplicatedException | LeadResponseException:
        """
        This method creates a new lead in Zoho CRM and updates the lead object with the new data.

        :return: A message with the result of the operation.
        """
        lead_dict = lead.as_zoho()

        try:
            message, data = self._create_record(module_name=self.api_name, data=lead_dict)
        except ModuleRecordDuplicatedException as e:
            raise LeadRecordDuplicatedException(e)

        except ModuleResponseException as e:
            raise LeadResponseException(e)

        # Update the lead structure with the new data
        for k, v in data.items():
            lead.add_or_update(k, v)

        return message

    def update(self, lead: Lead) -> str | LeadResponseException:
        """
        This method updates a lead in Zoho CRM.

        :return: A message with the result of the operation.
        """
        lead_dict = lead.as_zoho()

        try:
            message = self._update_record(module_name=self.api_name, record_id=lead.identifier, data=lead_dict)
        except ModuleResponseException as e:
            raise LeadResponseException(e)

        return message


__all__ = ("ZohoLeads", "Lead")
