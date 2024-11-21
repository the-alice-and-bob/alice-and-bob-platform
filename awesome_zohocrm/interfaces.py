import dataclasses

from dataclasses import dataclass

import abc
import requests
from datetime import datetime
from typing import Iterable, List, Tuple, Dict, Optional

# from zcrmsdk.src.com.zoho.crm.api.record import Record, RecordOperations as ZohoRecordOperations
# from zohocrmsdk.src.com.zoho.crm.api.tags import Tag
# from zohocrmsdk.src.com.zoho.crm.api import ParameterMap, HeaderMap, Param
# from zohocrmsdk.src.com.zoho.crm.api.record import RecordOperations, GetRecordsParam, GetRecordsHeader, SearchRecordsParam, BodyWrapper, \
#     ActionWrapper, SuccessResponse, APIException, Consent, Record


# from zcrmsdk.src.com.zoho.crm.api import HeaderMap, ParameterMap
# from zcrmsdk.src.com.zoho.crm.api.util import Choice, StreamWrapper
# from zcrmsdk.src.com.zoho.crm.api.record import Record as ZCRMRecord

from .auth import Auth


class ModuleException(Exception):
    ...


class ModuleRecordNotFound(Exception):
    ...


class ModuleRecordDuplicatedException(Exception):
    ...


class RecordInterface(abc.ABC):

    @classmethod
    def from_object(cls, fields: dict, input_data) -> dict:
        if isinstance(input_data, dict):
            ret = {}

            for k, v in fields.items():
                try:
                    ret[k] = input_data[v]
                except KeyError:
                    continue

            return ret

        else:
            return {
                k: getattr(input_data, v)
                for k, v in fields.items()
            }

    def as_zoho(self, input_data: Optional[dict] = None) -> dict:
        input_data = input_data or self

        if isinstance(input_data, dict):
            ret = {}

            for k, v in input_data.items():
                try:
                    ret[self.zoho_map[k]] = v
                except KeyError:
                    continue

            return ret

        else:
            return {
                k: getattr(input_data, v)
                for k, v in self.zoho_map.items()
            }

    @property
    @abc.abstractmethod
    def zoho_map(self) -> dict:
        raise NotImplementedError


class ModuleInterface(abc.ABC):

    @abc.abstractmethod
    def get_all(self) -> Iterable[dict]:
        ...

    @abc.abstractmethod
    def get_by_id(self, record_id: int) -> object:
        ...

    @abc.abstractmethod
    def create(self, data: dict) -> bool:
        ...

    @abc.abstractmethod
    def update(self, record_id: int, data: dict) -> bool:
        ...

    @abc.abstractmethod
    def delete(self, record_id: int) -> bool:
        ...


@dataclass
class Tag:
    identifier: int
    name: str
    color: str = None

    @classmethod
    def from_zoho_api(cls, data: dict):
        return cls(
            identifier=data.get("id"),
            name=data.get("name"),
            color=data.get("color")
        )


@dataclass
class ModuleMetadata:
    api_name: str
    field_name: str
    display_label: str
    identifier: int

    def __str__(self):
        return f"{self.display_label} (API Name: {self.api_name})"

    def __repr__(self):
        return f"<ModuleMetadata {self.display_label} (API Name: {self.api_name})>"


class BaseModule:

    def __init__(
            self,
            auth: Auth,
            name: str,
            identifier: int,
            api_name: str = None,
            label_singular: str = None,
            label_plural: str = None,
            web_link: str = None,
            modified: datetime = None,
            is_editable: bool = None,
            is_deletable: bool = None,
            is_viewable: bool = None,
            is_visible: bool = None
    ):
        """
        Estas propiedades también:
        print("BaseModule ID: " + str(module.get_id()))
        print("BaseModule API Name: " + str(module.get_api_name()))
        print("BaseModule Name: " + str(module.get_module_name()))
        print("BaseModule Is Convertable: " + str(bool(module.get_convertable())))
        print("BaseModule Is editable: " + str(bool(module.get_editable())))
        print("BaseModule Is deletable: " + str(bool(module.get_deletable())))
        print("BaseModule Web Link: " + str(module.get_web_link()))
        print("BaseModule Singular Label: " + str(module.get_singular_label()))
        if module.get_modified_time() is not None:
            print("BaseModule Modified Time: " + str(module.get_modified_time()))
        print("BaseModule Is viewable: " + str(bool(module.get_viewable())))
        print("BaseModule Is API supported: " + str(bool(module.get_api_supported())))
        print("BaseModule Is creatable: " + str(module.get_creatable()))
        print("BaseModule Plural Label: " + str(bool(module.get_plural_label())))
        print("BaseModule Generated Type: " + str(bool(module.get_generated_type())))
        print("BaseModule Is blueprintsupported: " + str(bool(module.get_isblueprintsupported())))
        print("BaseModule is Visible: " + str(bool(module.get_visible())))
        """
        self.auth = auth
        self.name = name
        self.identifier = identifier
        self.api_name = api_name
        self.label_singular = label_singular
        self.label_plural = label_plural
        self.web_link = web_link
        self.modified = modified
        self.is_editable = is_editable
        self.is_deletable = is_deletable
        self.is_viewable = is_viewable
        self.is_visible = is_visible

    @classmethod
    def from_api(cls, auth, data: dict):
        """
        Example:

        data = {
            'private_profile': None, 'global_search_supported': True, 'activity_badge': 'Enabled', '$field_states': ['convert_scheduler'], 'recycle_bin_on_delete': True, 'plural_label': 'Leads', 'presence_sub_menu': True, 'chart_view': False, 'id': '738692000000000043', 'per_page': 100, '$properties': ['$approval_state', '$wizard_connection_path', '$converted_detail', '$cpq_executions', '$currency_symbol', '$zia_owner_assignment', '$review', '$review_process', '$approval', '$in_merge', '$process_flow', '$orchestration', '$pathfinder', '$zia_visions', '$editable', '$field_states', '$locked_for_me', '$sharing_permission'], 'visibility': 1, 'sub_menu_available': True, 'profiles': [{'name': 'Administrator', 'id': '738692000000026972'}, {'name': 'Standard', 'id': '738692000000026974'}], '$on_demand_properties': ['$blocked_reason', '$client_portal_invited'], 'kanban_view_supported': True, 'web_link': None, 'lookup_field_properties': {'fields': [{'sequence_number': 1, 'api_name': 'Full_Name', 'id': '738692000000000595'}, {'sequence_number': 2, 'api_name': 'Email', 'id': '738692000000000599'}, {'sequence_number': 3, 'api_name': 'Tag', 'id': '738692000000069041'}, {'sequence_number': 4, 'api_name': 'Lead_Source', 'id': '738692000000000609'}, {'sequence_number': 5, 'api_name': 'First_Name', 'id': '738692000000000591'}, {'sequence_number': 6, 'api_name': 'Last_Name', 'id': '738692000000000593'}]}, 'viewable': True, 'api_name': 'Leads', 'public_fields_configured': False, 'module_function': 'Leads', 'chart_view_supported': True, 'custom_view': {'display_value': 'All Leads', 'created_time': None, 'access_type': 'public', 'criteria': {'comparator': 'equal', 'field': {'api_name': 'Converted__s', 'id': '738692000000263001'}, 'type': 'value', 'value': False}, 'system_name': 'ALLVIEWS', 'sort_by': None, 'created_by': None, 'shared_to': None, 'default': True, 'modified_time': '2024-11-12T13:00:27+01:00', 'name': 'All Open Leads', 'system_defined': True, 'modified_by': {'name': 'Daniel García', 'id': '738692000000414001'}, 'id': '738692000000030939', 'fields': [{'api_name': 'Full_Name', '_pin': False, 'id': '738692000000000595'}, {'api_name': 'Email', '_pin': False, 'id': '738692000000000599'}, {'api_name': 'Tag', '_pin': False, 'id': '738692000000069041'}, {'api_name': 'Lead_Source', '_pin': False, 'id': '738692000000000609'}, {'api_name': 'First_Name', '_pin': False, 'id': '738692000000000591'}, {'api_name': 'Last_Name', '_pin': False, 'id': '738692000000000593'}], 'category': 'public_views', 'last_accessed_time': '2024-11-13T15:37:06+01:00', 'locked': False, 'sort_order': None, 'favorite': None}, 'parent_module': {}, 'status': 'visible', 'has_more_profiles': False, 'access_type': 'org_based', 'kanban_view': False, 'deletable': True, 'description': None, 'creatable': True, 'filter_status': True, 'modified_time': '2024-10-08T14:39:26+02:00', 'actual_plural_label': 'Leads', 'lookupable': True, 'isBlueprintSupported': True, 'related_list_properties': {'sort_by': None, 'fields': ['Full_Name', 'Company', 'Email', 'Lead_Source', 'Lead_Status', 'Phone'], 'sort_order': None}, 'convertable': True, 'editable': True, 'actual_singular_label': 'Lead', 'display_field': 'Full_Name', 'search_layout_fields': ['Owner', 'Company', 'Full_Name', 'Email', 'Phone', 'Lead_Source'], 'show_as_tab': True, 'sequence_number': 2, 'singular_label': 'Lead', 'api_supported': True, 'quick_create': True, 'modified_by': {'name': 'Daniel García', 'id': '738692000000414001'}, 'generated_type': 'default', 'feeds_required': False, 'arguments': [], 'profile_count': 2, 'business_card_field_limit': 5
        }
        """
        return cls(
            auth=auth,
            name=data.get("module_function"),
            identifier=data.get("id"),
            api_name=data.get("api_name"),
            label_singular=data.get("singular_label"),
            label_plural=data.get("plural_label"),
            web_link=data.get("web_link"),
            modified=datetime.fromisoformat(data.get("modified_time")) if data.get("modified_time") else None,
            is_editable=data.get("editable"),
            is_deletable=data.get("deletable"),
            is_viewable=data.get("viewable"),
            is_visible=data.get("visibility"),
        )

    @staticmethod
    def _parse_tags(record: dict) -> dict:
        record["tags"] = [
            {
                "id": tag.get_id(),
                "name": tag.get_name()
            }
            for tag in record.get_key_value("Tag") or []
        ]

        try:
            del record["Tag"]
        except KeyError:
            ...

        return record

    def get_module_fields(self) -> Iterable[ModuleMetadata]:
        url = f"{self.auth.api_domain}/crm/v7/settings/fields?module={self.api_name}"

        response = requests.get(url, headers=self.auth.http_headers)

        if response.status_code != 200:
            raise ModuleException(f"Error getting fields: {response.text}")

        response_json = response.json()

        try:
            fields = response_json["fields"]
        except KeyError:
            raise ModuleException(f"Error getting fields: {response.text}")

        for f in fields:
            yield ModuleMetadata(
                api_name=f.get("api_name"),
                field_name=f.get("field_name"),
                display_label=f.get("display_label"),
                identifier=f.get("id")
            )

        return response_json

    def _get_records(
            self,
            module_name: str,
            return_fields: Iterable[str],
            date_start: datetime = None,
            date_end: datetime = None,
            query_params: dict = None,
            *,
            per_page: int = 50,
    ) -> Iterable[dict]:
        """
        Get Records of the module

        Example:

        >>> fields = ['id', 'First Name', 'Last Name', 'Email', 'Phone', 'Company', 'Created Time', 'Tag']
        >>> for record in module._get_records('Leads', fields):
        >>>     print(record)

        :param module_name: the name of the module. For example: Leads, Contacts, Accounts, etc.
        :param page: the page number of the results. Default is 1.
        :param per_page: the number of records per page. Default is 120.
        :param return_fields: the fields to retrieve from the records.
        :param date_start: the start date to filter the records. Default is None.
        :param date_end: the end date to filter the records. Default is None.

        :return: an iterable of records. Each record is a dictionary with the field names as keys.
        """

        current_page = 1

        url = f"{self.auth.api_domain}/crm/v7/{module_name}"

        query_params = query_params or {}
        query_params.update({
            "page": 1,
            "per_page": 50,
            "fields": ",".join(return_fields)
        })

        while True:

            response = requests.get(url, headers=self.auth.http_headers, params=query_params)

            if response.status_code != 200:
                raise ModuleException(f"Error getting leads: {response.text}")

            """
            Json data example:

            {
                "data": [
                    {
                        "Converted_Date_Time": "2022-11-21T15:12:13+05:30",
                        "Email": null,
                        "Last_Name": "test8000",
                        "id": "3652397000009851001",
                        "Record_Status__s": "Available",
                        "Converted__s": true
                    },
                    {
                        "Converted_Date_Time": "2022-11-21T15:12:13+05:30",
                        "Email": null,
                        "Last_Name": "test7000",
                        "id": "3652397000009850001",
                        "Record_Status__s": "Available",
                        "Converted__s": true
                    },
                    {
                        "Converted_Date_Time": "2022-11-21T11:34:37+05:30",
                        "Email": null,
                        "Last_Name": "test6000",
                        "id": "3652397000009843012",
                        "Record_Status__s": "Available",
                        "Converted__s": true
                    },
                    {
                        "Converted_Date_Time": "2022-11-21T11:34:36+05:30",
                        "Email": null,
                        "Last_Name": "test3000",
                        "id": "3652397000009843001",
                        "Record_Status__s": "Available",
                        "Converted__s": true
                    },
                    {
                        "Converted_Date_Time": "2022-11-21T22:47:16+05:30",
                        "Email": null,
                        "Last_Name": "test2000",
                        "id": "3652397000009836003",
                        "Record_Status__s": "Available",
                        "Converted__s": true
                    }
                ],
                "info": {
                    "call": false,
                    "per_page": 5,
                    "next_page_token": "c8582xx9e7c7",
                    "count": 5,
                    "sort_by": "id",
                    "page": 1,
                    "previous_page_token": null,
                    "page_token_expiry": "2022-11-11T15:08:14+05:30",
                    "sort_order": "desc",
                    "email": false,
                    "more_records": true
                }
            }
            """
            response_json = response.json()

            try:
                data = response_json["data"]
            except KeyError:
                break

            yield from data

            # Getting info
            if response_json.get("info", {}).get("more_records") is False:
                break
            else:
                current_page += 1
                query_params.update({"page": current_page})

    def _search_by_id(
            self,
            record_id: int,
            module_name: str,
            return_fields: Iterable[str],
            date_start: datetime = None,
            date_end: datetime = None,
            query_params: dict = None,
    ) -> dict:
        """
        Search for a record in the module

        Example:

        >>> fields = ['id', 'First Name', 'Last Name', 'Email', 'Phone', 'Company', 'Created Time', 'Tag']
        >>> for record in module._search_by_id(12112312312, 'Leads', fields):
        >>>     print(record)

        :param email: the email to search for. This is a required parameter.
        :param module_name: the name of the module. For example: Leads, Contacts, Accounts, etc.
        :param page: the page number of the results. Default is 1.
        :param per_page: the number of records per page. Default is 120.
        :param return_fields: the fields to retrieve from the records.
        :param date_start: the start date to filter the records. Default is None.
        :param date_end: the end date to filter the records. Default is None.
        :param additional_record_operations: additional operations to perform on the records.
        """
        url = f"{self.auth.api_domain}/crm/v7/{module_name}/{record_id}"

        query_params = query_params or {}
        query_params.update({
            "fields": ",".join(return_fields)
        })

        response = requests.get(url, headers=self.auth.http_headers, params=query_params)

        if response.status_code == 204:
            raise ModuleRecordNotFound(f"Record with ID {record_id} not found")

        if response.status_code != 200:
            raise ModuleException(f"Error getting record: {response.text}")

        response_json = response.json()

        try:
            data = response_json["data"][0]
        except (KeyError, IndexError):
            raise ModuleRecordNotFound(f"Record with ID {record_id} not found")

        return data

    def _search_by_field(
            self,
            criteria: List[Tuple[str, str, str]],
            module_name: str,
            return_fields: Iterable[str],
            query_params: dict = None,
            multiple_response: bool = False,
    ) -> dict:
        """

        fields parameter example:

        fields = [("email", "equals", "aa@aa.com")]


        :param email: the email to search for. This is a required parameter.
        :param module_name: the name of the module. For example: Leads, Contacts, Accounts, etc.
        :param page: the page number of the results. Default is 1.
        :param per_page: the number of records per page. Default is 120.
        :param return_fields: the fields to retrieve from the records.
        :param date_start: the start date to filter the records. Default is None.
        :param date_end: the end date to filter the records. Default is None.
        :param additional_record_operations: additional operations to perform on the records.
        """
        # Transform fields into a query string.
        #
        # Example with len 1:
        #   fields = email:equals:aaa@aaa.com
        # Example with len 2 or more:
        #   fields = (email:equals:aaaa@aaaa.com)and(name:eq:John)
        if len(criteria) == 1:
            query_string = f"{criteria[0][0]}:{criteria[0][1]}:{criteria[0][2]}"
        else:
            query_string = "(" + ")and(".join([f"{f[0]}:{f[1]}:{f[2]}" for f in criteria]) + ")"

        url = f"{self.auth.api_domain}/crm/v7/{module_name}/search?criteria={query_string}"

        query_params = query_params or {}
        query_params.update({
            "fields": ",".join(return_fields)
        })

        response = requests.get(url, headers=self.auth.http_headers, params=query_params)

        if response.status_code != 200:
            raise ModuleException(f"Error getting records: {response.text}")

        response_json = response.json()

        try:
            if multiple_response:
                return response_json["data"]

            else:
                data = response_json["data"][0]
        except (KeyError, IndexError):
            raise ModuleRecordNotFound(f"Record with not found")

        return data

    def _search_by_email(
            self,
            email: str,
            module_name: str,
            return_fields: Iterable[str],
            date_start: datetime = None,
            date_end: datetime = None,
            query_params: dict = None,
    ) -> dict:
        """
        :param email: the email to search for. This is a required parameter.
        :param module_name: the name of the module. For example: Leads, Contacts, Accounts, etc.
        :param page: the page number of the results. Default is 1.
        :param per_page: the number of records per page. Default is 120.
        :param return_fields: the fields to retrieve from the records.
        :param date_start: the start date to filter the records. Default is None.
        :param date_end: the end date to filter the records. Default is None.
        :param additional_record_operations: additional operations to perform on the records.
        """
        url = f"{self.auth.api_domain}/crm/v7/{module_name}/search?email={email}"

        query_params = query_params or {}
        query_params.update({
            "fields": ",".join(return_fields)
        })

        response = requests.get(url, headers=self.auth.http_headers, params=query_params)

        if response.status_code == 204:
            raise ModuleRecordNotFound(f"Record with email {email} not found")

        if response.status_code != 200:
            raise ModuleException(f"Error getting leads: {response.text}")

        response_json = response.json()

        try:
            data = response_json["data"][0]
        except (KeyError, IndexError):
            raise ModuleRecordNotFound(f"Record with ID {email} not found")

        return data

    def _create_record(self, module_name: str, data: Dict[str, str]) -> int:
        """
        Create a record in the module with the data

        :return: returns the record ID of the created record
        """
        url = f"{self.auth.api_domain}/crm/v7/{module_name}"

        # Clean None values
        data = {k: v for k, v in data.items() if v is not None}

        # Transform date format into Zoho format:

        post_data = {
            "data": [data]
        }

        response = requests.post(url, headers=self.auth.http_headers, json=post_data)

        if response.status_code == 400:
            if "DUPLICATE_DATA" in response.text:
                raise ModuleRecordDuplicatedException("Record already exists")

        if response.status_code != 201:
            raise ModuleException(f"Error creating record: {response.text}")

        response_json = response.json()

        try:
            return response_json["data"][0]["details"]["id"]
        except (KeyError, IndexError):
            raise ModuleRecordNotFound(f"Record not found")

    def _update_record(self, module_name: str, record_id: int, data: Dict[str, str]) -> dict:
        url = f"{self.auth.api_domain}/crm/v7/{module_name}/{record_id}"

        # Clean None values
        data = {k: v for k, v in data.items() if v is not None}

        post_data = {
            "data": [data],
            "details": data
        }

        response = requests.put(url, headers=self.auth.http_headers, json=post_data)

        if response.status_code in (404, 400):
            raise ModuleRecordNotFound(f"Record not found: {response.text}")

        if response.status_code != 200:
            raise ModuleException(f"Error creating record: {response.text}")

        response_json = response.json()

        try:
            return response_json["data"][0]["details"]
        except (KeyError, IndexError):
            raise ModuleRecordNotFound(f"Record not found")

    def _update_record_tag(self, module_name: str, record_id: str, tags: List[Tag]) -> dict:
        url = f"{self.auth.api_domain}/crm/v7/{module_name}/{record_id}/actions/add_tags"

        # Clean None values
        data = {
            "tags": [
                {
                    # "id": tag.identifier,
                    "name": tag.name,
                    "color": tag.color
                }
                for tag in tags
            ]
        }

        response = requests.post(url, headers=self.auth.http_headers, json=data)

        if response.status_code in (404, 400):
            raise ModuleRecordNotFound(f"Record not found: {response.text}")

        if response.status_code != 200:
            raise ModuleException(f"Error creating record: {response.text}")

        response_json = response.json()

        try:
            return response_json["data"][0]["details"]
        except (KeyError, IndexError):
            raise ModuleRecordNotFound(f"Record not found")

    def _delete_record(self, module_name: str, record_id: int | List[int] | Iterable[int]) -> None:

        if isinstance(record_id, int):
            record_ids = record_id

        elif isinstance(record_id, (list, tuple, set)):
            record_ids = ",".join(str(i) for i in record_id)
        else:
            raise ValueError("record_id must be an integer or a list of integers")

        url = f"{self.auth.api_domain}/crm/v7/{module_name}?ids={record_ids}"

        response = requests.delete(url, headers=self.auth.http_headers)

        if response.status_code == 404:
            raise ModuleRecordNotFound(f"Record not found: {response.text}")

        if response.status_code == 400:
            raise ModuleRecordNotFound(f"Record not found: {response.text}")

        if response.status_code != 200:
            raise ModuleException(f"Error deleting record: {response.text}")

    def _map_zoho_response_with_object(self, data: dict, klass, fields_map: dict) -> object:
        """
        Map the Zoho data to the object

        Example:

        >>> fields_map = {
        >>>     "id": "id",
        >>>     "First Name": "first_name",
        >>>     "Last Name": "last_name",
        >>>     "Email": "email",
        >>>     "Phone": "phone",
        >>>     "Company": "company",
        >>>     "Created Time": "created_time",
        >>>     "Tag": "tags"
        >>> }
        >>> lead = module._map_zoho_response_with_object(data, Lead, fields_map)

        :param data: the data from the Zoho API
        :param klass: the class to map the data
        :param fields_map: the fields map to map the data
        :return: the object with the data
        """
        config = {}

        for k, v in fields_map.items():
            # Map tags
            if "tag" in k.lower() and data.get("Tag", False):
                config[v] = [Tag.from_zoho_api(tag) for tag in data[k]]
                continue

            try:
                config[v] = data[k]
            except KeyError:
                continue

        return klass(**config)

    def __str__(self):
        return f"{self.name} ({self.identifier})"

    def __repr__(self):
        return f"<BaseModule {self.name} ({self.identifier})>"


__all__ = (
    'BaseModule', 'ModuleException', 'ModuleRecordNotFound', 'ModuleRecordDuplicatedException', 'ModuleInterface',
    'Tag', 'RecordInterface'
)
