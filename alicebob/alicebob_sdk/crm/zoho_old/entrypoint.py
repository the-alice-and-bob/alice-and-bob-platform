import tempfile
from typing import List

from zohocrmsdk.src.com.zoho.crm.api.modules import ModulesOperations

from .auth import *
from .leads import *
from .contacts import *
from .interfaces import *
from .purchase_orders import *

class ModulesNames:
    LEADS = "Leads"
    CONTACTS = "Contacts"
    PURCHASE_ORDERS = "Purchase_Orders"

class ZohoCRMException(Exception):
    ...


class ZohoCRM:

    def __init__(self, zoho_client_id, zoho_client_secret, zoho_grant_token, token_path: str = "zoho_tokens"):
        self.temp_dir = tempfile.TemporaryDirectory()

        initialize_zoho_sdk(
            zoho_client_id=zoho_client_id,
            zoho_client_secret=zoho_client_secret,
            zoho_grant_token=zoho_grant_token,
            token_path=token_path,
            resource_path=self.temp_dir.name
        )

    def get_modules(self) -> List[Module]:
        modules_operations = ModulesOperations()
        response = modules_operations.get_modules()
        if response is not None:
            response_object = response.get_object()

            for module in response_object.get_modules():
                yield Module(module, module.get_module_name(), module.get_id())

    def __get_module_by_name_in_zoho_format(self, module_name: str) -> object:
        modules_operations = ModulesOperations()
        response = modules_operations.get_module_by_api_name(module_name)
        if response is not None:
            response_object = response.get_object()
            try:
                module = response_object.get_modules()[0]
            except IndexError:
                raise ZohoCRMException(f"BaseModule {module_name} not found")

            return module

    def get_module(self, module_id: int) -> Module:
        modules_operations = ModulesOperations()
        response = modules_operations.get_module(module_id)
        if response is not None:
            response_object = response.get_object()

            try:
                module = response_object.get_modules()[0]
            except IndexError:
                raise ZohoCRMException(f"BaseModule {module_id} not found")

            return Module.from_zoho_object(module)

    def get_module_by_name(self, module_name: str) -> Module:
        return Module.from_zoho_object(
            self.__get_module_by_name_in_zoho_format(module_name)
        )

    def get_leads_module(self) -> ZohoLeads:
        m = self.__get_module_by_name_in_zoho_format(ModulesNames.LEADS)
        return ZohoLeads.from_zoho_object(m)

    def get_contacts_module(self) -> ZohoContacts:
        m = self.__get_module_by_name_in_zoho_format(ModulesNames.CONTACTS)
        return ZohoContacts.from_zoho_object(m)

    def get_purchase_orders_module(self) -> ZohoPurchaseOrders:
        m = self.__get_module_by_name_in_zoho_format(ModulesNames.PURCHASE_ORDERS)
        return ZohoPurchaseOrders.from_zoho_object(m)

    def __del__(self):
        self.temp_dir.cleanup()


__all__ = ("ZohoCRM",)
