import abc
from datetime import datetime
from typing import Iterable, List, Tuple, Dict

# from zcrmsdk.src.com.zoho.crm.api.record import Record, RecordOperations as ZohoRecordOperations
from zohocrmsdk.src.com.zoho.crm.api.tags import Tag
from zohocrmsdk.src.com.zoho.crm.api import ParameterMap, HeaderMap, Param
from zohocrmsdk.src.com.zoho.crm.api.record import RecordOperations, GetRecordsParam, GetRecordsHeader, SearchRecordsParam, BodyWrapper, \
    ActionWrapper, SuccessResponse, APIException, Consent, Record


# from zcrmsdk.src.com.zoho.crm.api import HeaderMap, ParameterMap
# from zcrmsdk.src.com.zoho.crm.api.util import Choice, StreamWrapper
# from zcrmsdk.src.com.zoho.crm.api.record import Record as ZCRMRecord

class ModuleException(Exception):
    ...


class ModuleRecordNotFound(Exception):
    ...

class ModuleRecordDuplicatedException(Exception):
    ...


class ModuleResponseException(Exception):

    def __init__(self, status: str, code: str, details: dict, message: str):
        self.status = status
        self.code = code
        self.details = details
        self.message = message

        super().__init__(f"Status: {status}, Code: {code}, Details: {details}, Message: {message}")


def parse_response(action_response) -> Tuple[str, dict] | ModuleResponseException | ModuleRecordDuplicatedException:
    if isinstance(action_response, SuccessResponse):
        details = action_response.get_details()

        ret = {
            key: str(value)
            for key, value in details.items()
        }

        return action_response.get_message().get_value(), ret

    # Check if the request returned an exception
    elif isinstance(action_response, APIException):

        if action_response.get_code().get_value() == 'DUPLICATE_DATA':
            raise ModuleRecordDuplicatedException("Record already exists")

        # Get the details dict
        details = action_response.get_details()

        error_details = {
            key: str(value)
            for key, value in details.items()
        }

        raise ModuleResponseException(
            status=action_response.get_status().get_value(),
            code=action_response.get_code().get_value(),
            details=error_details,
            message=action_response.get_message().get_value()
        )


class BaseModule:

    def __init__(
            self,
            obj,  # BaseModule
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
        self._obj = obj
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
    def from_zoho_object(cls, zoho_object):
        return cls(
            obj=zoho_object,
            name=zoho_object.get_module_name(),
            identifier=zoho_object.get_id(),
            api_name=zoho_object.get_api_name(),
            label_singular=zoho_object.get_singular_label(),
            label_plural=zoho_object.get_plural_label(),
            web_link=zoho_object.get_web_link(),
            modified=zoho_object.get_modified_time(),
            is_editable=zoho_object.get_editable(),
            is_deletable=zoho_object.get_deletable(),
            is_viewable=zoho_object.get_viewable(),
            is_visible=zoho_object.get_visible(),
        )

    @staticmethod
    def _prepare_request_parameters(
            page: int,
            per_page: int,
            field_names: List[str],
            date_start: datetime = None,
            date_end: datetime = None,
            additional_record_operations: List[Tuple[Param, str]] = None
    ) -> ParameterMap:

        param_instance = ParameterMap()
        param_instance.add(GetRecordsParam.page, page)
        param_instance.add(GetRecordsParam.per_page, per_page)

        if additional_record_operations is not None:
            for (operation, value) in additional_record_operations:
                param_instance.add(operation, value)

        for field in field_names:
            param_instance.add(GetRecordsParam.fields, field.replace(' ', '_'))
        # param_instance.add(GetRecordsParam.sort_by, 'Email')
        # param_instance.add(GetRecordsParam.sort_order, 'desc')

        if date_start is not None and isinstance(date_start, datetime):
            param_instance.add(GetRecordsParam.startdatetime, date_start)

        if date_end is not None and isinstance(date_end, datetime):
            param_instance.add(GetRecordsParam.enddatetime, date_end)

        param_instance.add(GetRecordsParam.include_child, "true")

        return param_instance

    @staticmethod
    def _prepare_request_headers() -> HeaderMap:
        header_instance = HeaderMap()
        # Possible headers for Get Records operation
        # header_instance.add(GetRecordsHeader.if_modified_since, datetime.fromisoformat('2020-01-01T00:00:00+05:30'))
        # header_instance.add(GetRecordsHeader.x_external, "Leads.External")
        # Call get_records method that takes ParameterMap Instance, HeaderMap Instance and module_api_name as parameters

        # header_instance.add(GetRecordsHeader.x_external, "Leads.External")
        # Call get_records method that takes ParameterMap Instance, HeaderMap Instance and module_api_name as parameters
        return header_instance

    @staticmethod
    def _manage_iterable_response(
            # record_operations: RecordOperations, param_instance: ParameterMap, header_instance: HeaderMap
            response
    ) -> Iterable[dict]:
        """
        This method to process the data and returns the list of obtained Record instances.
        """
        if response is not None:

            if response.get_status_code() in (204, 304):
                raise ModuleException('No Content' if response.get_status_code() == 204 else 'Not Modified')

            if response.get_status_code() != 200:
                raise ModuleException(f"Status Code: {response.get_status_code()}")

            response_object = response.get_object()
            if response_object is not None:
                record_list = response_object.get_data()

                for record in record_list:
                    v: dict = record.get_key_values()

                    yield v

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

    @staticmethod
    def _manage_single_response(
            record_id: int, record_operations: RecordOperations, param_instance: ParameterMap, header_instance: HeaderMap
    ) -> dict:
        response = record_operations.get_record(record_id, param_instance, header_instance)

        if response is not None:
            if response.get_status_code() in (204, 304):
                raise ModuleException('No Content' if response.get_status_code() == 204 else 'Not Modified')

            if response.get_status_code() != 200:
                raise ModuleException(f"Status Code: {response.get_status_code()}")

            response_object = response.get_object()
            if response_object is not None:
                try:
                    record = response_object.get_data()[0]
                except IndexError:
                    raise ModuleRecordNotFound(f"Record with ID {record_id} not found")

                v: dict = record.get_key_values()
                v["tags"] = [
                    {
                        "id": tag.get_id(),
                        "name": tag.get_name()
                    }
                    for tag in record.get_key_value("Tag") or []
                ]
                del v["Tag"]

                return v

    def _get_records(
            self,
            module_name: str,
            return_fields: List[str],
            date_start: datetime = None,
            date_end: datetime = None,
            *,
            per_page: int = 50,
            additional_record_operations: List[Tuple[Param, str]] = None,
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
        while True:
            record_operations = RecordOperations(module_name)

            param_instance = self._prepare_request_parameters(
                page=current_page,
                per_page=per_page,
                field_names=return_fields,
                date_start=date_start,
                date_end=date_end,
                additional_record_operations=additional_record_operations
            )

            header_instance = self._prepare_request_headers()

            response = record_operations.get_records(param_instance, header_instance)

            yield from self._manage_iterable_response(response)

            # Recover page info
            try:
                info = response.get_object().get_info()
                if not info.get_more_records():
                    break
            except AttributeError:
                break

            current_page += 1

    def _search_by_email(
            self,
            email: str,
            module_name: str,
            return_fields: List[str],
            date_start: datetime = None,
            date_end: datetime = None,
            additional_record_operations: List[Tuple[Param, str]] = None,
    ) -> dict:
        """
        Search for a record in the module

        Example:

        >>> fields = ['id', 'First Name', 'Last Name', 'Email', 'Phone', 'Company', 'Created Time', 'Tag']
        >>> for record in module._search_by_email('demo@demo.com', 'Leads', fields):
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

        record_operations = RecordOperations(module_name)
        param_instance = self._prepare_request_parameters(
            page=1,
            per_page=5,
            field_names=return_fields,
            date_start=date_start,
            date_end=date_end,
            additional_record_operations=additional_record_operations
        )

        header_instance = self._prepare_request_headers()

        # Add search parameters
        param_instance.add(SearchRecordsParam.email, email)

        for x in self._manage_iterable_response(record_operations, param_instance, header_instance):
            return x
        else:
            raise ModuleRecordNotFound(f"Record with email {email} not found")

    def _search_by_id(
            self,
            record_id: int,
            module_name: str,
            return_fields: List[str],
            date_start: datetime = None,
            date_end: datetime = None,
            additional_record_operations: List[Tuple[Param, str]] = None,
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

        record_operations = RecordOperations(module_name)
        param_instance = self._prepare_request_parameters(
            page=1,
            per_page=5,
            field_names=return_fields,
            date_start=date_start,
            date_end=date_end,
            additional_record_operations=additional_record_operations
        )

        header_instance = self._prepare_request_headers()

        if found := self._manage_single_response(record_id, record_operations, param_instance, header_instance):
            return found
        else:
            raise ModuleRecordNotFound(f"Record with ID {module_name} not found")

    @staticmethod
    def _create_record(module_name: str, data: Dict[str, object]):
        record_operations = RecordOperations(module_name)

        request = BodyWrapper()

        # List to hold Record instances
        records_list = []

        # Get instance of Record Class
        record = Record()

        for k, v in data.items():
            if v is None:
                continue

            if k == 'tags':
                tags_list = []

                for tag in v:
                    tag_instance = Tag()
                    tag_instance.set_name(tag)
                    tags_list.append(tag_instance)

                record.add_key_value('Tag', tags_list)
                continue

            record.add_key_value(k, v)

        # Tags of th
        # Add Record instance to the list
        records_list.append(record)

        # Set the list to data in BodyWrapper instance
        request.set_data(records_list)

        header_instance = HeaderMap()

        # Call create_records method that takes BodyWrapper instance and module_api_name as parameters
        response = record_operations.create_records(request, header_instance)

        if response is not None:
            # Get the status code from data
            print('Status Code: ' + str(response.get_status_code()))

            # Get object from data
            response_object = response.get_object()

            if response_object is not None:

                # Check if expected ActionWrapper instance is received.
                if isinstance(response_object, ActionWrapper):

                    # Get the list of obtained ActionResponse instances
                    action_response_list = response_object.get_data()

                    for action_response in action_response_list:
                        return parse_response(action_response)

    @staticmethod
    def _update_record(module_name: str, record_id: int, data: Dict[str, object]):
        record_operations = RecordOperations(module_name)

        request = BodyWrapper()

        # List to hold Record instances
        records_list = []

        # Get instance of Record Class
        record = Record()

        for k, v in data.items():
            if v is None:
                continue

            if k == 'tags':
                tags_list = []

                for tag in v:
                    tag_instance = Tag()
                    tag_instance.set_name(tag)
                    tags_list.append(tag_instance)

                record.add_key_value('Tag', tags_list)
                continue

            record.add_key_value(k, v)

        # Add Record instance to the list
        records_list.append(record)

        # Set the list to data in BodyWrapper instance
        request.set_data(records_list)

        header_instance = HeaderMap()

        # Call create_records method that takes BodyWrapper instance and module_api_name as parameters
        response = record_operations.update_record(record_id, request, header_instance)

        if response is not None:
            # Get object from data
            response_object = response.get_object()

            if response_object is not None:

                # Check if expected ActionWrapper instance is received.
                if isinstance(response_object, ActionWrapper):

                    # Get the list of obtained ActionResponse instances
                    action_response_list = response_object.get_data()

                    for action_response in action_response_list:
                        return parse_response(action_response)

    def __str__(self):
        return f"{self.name} ({self.identifier})"

    def __repr__(self):
        return f"<BaseModule {self.name} ({self.identifier})>"


__all__ = ('Module', 'ModuleException', 'ModuleRecordNotFound', 'ModuleRecordDuplicatedException', 'ModuleResponseException')
