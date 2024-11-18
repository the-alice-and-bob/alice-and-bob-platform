from datetime import datetime
from typing import Iterable, List
from dataclasses import dataclass, field

import requests

from .interfaces import *
from ...notion import NOTION_TOKEN


class LeadResponseException(Exception):
    ...


class LeadDuplicatedException(Exception):
    ...


class LeadNotFoundException(Exception):
    ...


FIELD_MAP = {
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
    "Created_Time": "created_time",
    "Modified_Time": "modified_time",
}


@dataclass
class Lead(RecordInterface):
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

    @staticmethod
    def zoho_map() -> dict:
        return FIELD_MAP


class ZohoLeads(BaseModule, ModuleInterface):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_all(self) -> Iterable[Lead]:
        query_params = {
            "approved": "true",
            "converted": "false",
        }
        for found in super()._get_records(module_name=self.api_name, return_fields=FIELD_MAP.keys(), query_params=query_params):
            yield super()._map_zoho_response_with_object(found, Lead, FIELD_MAP)

    def get_by_email(self, email: str) -> Lead | LeadNotFoundException:

        try:
            if found := self._search_by_email(email=email, module_name=self.api_name, return_fields=FIELD_MAP.keys()):
                yield super()._map_zoho_response_with_object(found, Lead, FIELD_MAP)
        except ModuleRecordNotFound:
            raise LeadNotFoundException(f"Lead with email {email} not found")

    def get_by_id(self, record_id: int) -> Lead | LeadNotFoundException:
        try:
            if found := self._search_by_id(record_id=record_id, module_name=self.api_name, return_fields=FIELD_MAP.keys()):
                return super()._map_zoho_response_with_object(found, Lead, FIELD_MAP)
        except ModuleRecordNotFound:
            raise LeadNotFoundException(f"Lead with id {record_id} not found")

    def create(self, lead: Lead) -> bool | LeadDuplicatedException | LeadResponseException | None:
        """
        This method creates a new lead in Zoho CRM and updates the lead object with the new data.

        :return: A message with the result of the operation.
        """
        lead_dict = Lead.as_zoho(lead, Lead)

        try:
            self._create_record(module_name=self.api_name, data=lead_dict)
        except ModuleRecordDuplicatedException as e:
            raise LeadDuplicatedException(e)

        except ModuleException as e:
            raise LeadResponseException(e)

        return True

    def convert_lead(self, lead: Lead | int):
        if isinstance(lead, Lead):
            lead_id = lead.identifier
        else:
            lead_id = lead

        # First get lead options
        url = f"{self.auth.api_domain}/crm/v7/Leads/{lead_id}/__conversion_options"

        response = requests.get(url, headers=self.auth.http_headers)

        if response.status_code == 204:
            account = None

        elif response.status_code == 200:
            response_json = response.json()

            try:
                account = response_json.get("Accounts")[0]["id"]
            except (IndexError, KeyError):
                account = None

        elif response.status_code == 400:
            raise LeadNotFoundException(response.text)

        else:
            raise LeadResponseException(response.text)

        data = {
            "overwrite": False,
            "notify_lead_owner": False,
            "notify_new_entity_owner": False,
            "move_attachments_to": {
                "api_name": "Deals"
            }
        }

        if account:
            data["Accounts"]["id"] = account

        url = f"{self.auth.api_domain}/crm/v7/Leads/{lead_id}/actions/convert"

        body = {
            "data": [data]
        }

        response = requests.post(url, headers=self.auth.http_headers, json=body)

        if response.status_code == 400:
            raise LeadDuplicatedException(response.json())

        if response.status_code != 200:
            raise LeadResponseException(response.json())

        return True

    def update(self, record_id: int, **kwargs) -> bool | LeadResponseException | LeadNotFoundException:
        """
        This method updates a lead in Zoho CRM.

        :return: A message with the result of the operation.
        """

        lead_dict = Lead.as_zoho(kwargs, Lead)

        try:
            self._update_record(module_name=self.api_name, record_id=record_id, data=lead_dict)
        except ModuleRecordDuplicatedException as e:
            raise LeadNotFoundException(e)

        except ModuleException as e:
            raise LeadResponseException(e)

        return True

    def delete(self, record_id: int) -> bool | LeadNotFoundException:
        try:
            self._delete_record(module_name=self.api_name, record_id=record_id)
        except ModuleRecordNotFound:
            raise LeadNotFoundException(f"Lead with id {record_id} not found")

        return True


__all__ = ("ZohoLeads", "Lead", "Tag", "LeadNotFoundException", "LeadDuplicatedException", "LeadResponseException")
