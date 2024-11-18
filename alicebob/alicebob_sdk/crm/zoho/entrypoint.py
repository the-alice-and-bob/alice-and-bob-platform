import tempfile
from typing import List

from .auth import *
from .leads import *
from .contacts import *
from .products import *
from .interfaces import *
from .purchase_orders import *
from .course_progress import *

"""
https://www.zoho.com/crm/developer/docs/api/v7/
"""


class ModulesNames:
    LEADS = "Leads"
    CONTACTS = "Contacts"
    PURCHASE_ORDERS = "Purchase_Orders"
    PRODUCTS = "Products"
    COURSE_PROGRESS = "Course_Progress"


class ZohoCRMException(Exception):
    ...


class ZohoCRM:

    def __init__(self, auth: Auth = None):
        self.auth = auth or Auth()

        # Ensure token is valid
        self.auth.ping()

    def get_modules(self) -> List[BaseModule]:

        modules_url = f"{self.auth.api_domain}/crm/v7/settings/modules"

        response = requests.get(modules_url, headers=self.auth.http_headers)

        if response.status_code != 200:
            raise ZohoCRMException(f"Error getting modules: {response.text}")

        """
        Response in JSON:

        {
        "modules":
            [
                {
                    "has_more_profiles": false,
                    "access_type": "org_based",
                    "private_profile": null,
                    "global_search_supported": false,
                    "deletable": false,
                    "description": null,
                    "creatable": false,
                    "recycle_bin_on_delete": false,
                    "modified_time": null,
                    "plural_label": "Home",
                    "presence_sub_menu": false,
                    "actual_plural_label": "Home",
                    "lookupable": false,
                    "id": "738692000000000041",
                    "isBlueprintSupported": false,
                    "visibility": 1,
                    "convertable": false,
                    "sub_menu_available": false,
                    "editable": false,
                    "actual_singular_label": "Home",
                    "profiles":
                    [
                        {
                            "name": "Administrator",
                            "id": "738692000000026972"
                        },
                        {
                            "name": "Standard",
                            "id": "738692000000026974"
                        }
                    ],
                    "show_as_tab": true,
                    "web_link": null,
                    "sequence_number": 1,
                    "singular_label": "Home",
                    "viewable": true,
                    "api_supported": false,
                    "api_name": "Home",
                    "quick_create": false,
                    "modified_by": null,
                    "generated_type": "default",
                    "feeds_required": false,
                    "public_fields_configured": false,
                    "arguments":
                    [],
                    "module_name": "Home",
                    "profile_count": 2,
                    "business_card_field_limit": 5,
                    "parent_module":
                    {},
                    "status": "visible"
                },
                {
                    "has_more_profiles": false,
                    "access_type": "org_based",
                    "private_profile": null,
                    "global_search_supported": true,
                    "deletable": true,
                    "description": null,
                    "creatable": true,
                    "recycle_bin_on_delete": true,
                    "modified_time": "2024-10-08T14:39:26+02:00",
                    "plural_label": "Leads",
                    "presence_sub_menu": true,
                    "actual_plural_label": "Leads",
                    "lookupable": true,
                    "id": "738692000000000043",
                    "isBlueprintSupported": true,
                    "visibility": 1,
                    "convertable": true,
                    "sub_menu_available": true,
                    "editable": true,
                    "actual_singular_label": "Lead",
                    "profiles":
                    [
                        {
                            "name": "Administrator",
                            "id": "738692000000026972"
                        },
                        {
                            "name": "Standard",
                            "id": "738692000000026974"
                        }
                    ],
                    "show_as_tab": true,
                    "web_link": null,
                    "sequence_number": 2,
                    "singular_label": "Lead",
                    "viewable": true,
                    "api_supported": true,
                    "api_name": "Leads",
                    "quick_create": true,
                    "modified_by":
                    {
                        "name": "Daniel García",
                        "id": "738692000000414001"
                    },
                    "generated_type": "default",
                    "feeds_required": false,
                    "public_fields_configured": false,
                    "arguments":
                    [],
                    "module_name": "Leads",
                    "profile_count": 2,
                    "business_card_field_limit": 5,
                    "parent_module":
                    {},
                    "status": "visible"
                },
                {
                    "has_more_profiles": false,
                    "access_type": "org_based",
                    "private_profile": null,
                    "global_search_supported": true,
                    "deletable": true,
                    "description": null,
                    "creatable": true,
                    "recycle_bin_on_delete": true,
                    "modified_time": "2024-11-12T17:13:50+01:00",
                    "plural_label": "Contacts",
                    "presence_sub_menu": true,
                    "actual_plural_label": "Contacts",
                    "lookupable": true,
                    "id": "738692000000000047",
                    "isBlueprintSupported": true,
                    "visibility": 1,
                    "convertable": false,
                    "sub_menu_available": true,
                    "editable": true,
                    "actual_singular_label": "Contact",
                    "profiles":
                    [
                        {
                            "name": "Administrator",
                            "id": "738692000000026972"
                        },
                        {
                            "name": "Standard",
                            "id": "738692000000026974"
                        }
                    ],
                    "show_as_tab": true,
                    "web_link": null,
                    "sequence_number": 3,
                    "singular_label": "Contact",
                    "viewable": true,
                    "api_supported": true,
                    "api_name": "Contacts",
                    "quick_create": true,
                    "modified_by":
                    {
                        "name": "Daniel García",
                        "id": "738692000000414001"
                    },
                    "generated_type": "default",
                    "feeds_required": false,
                    "public_fields_configured": false,
                    "arguments":
                    [],
                    "module_name": "Contacts",
                    "profile_count": 2,
                    "business_card_field_limit": 5,
                    "parent_module":
                    {},
                    "status": "visible"
                },
                {
                    "has_more_profiles": false,
                    "access_type": "org_based",
                    "private_profile": null,
                    "global_search_supported": true,
                    "deletable": true,
                    "description": null,
                    "creatable": true,
                    "recycle_bin_on_delete": true,
                    "modified_time": "2024-09-27T14:46:48+02:00",
                    "plural_label": "Accounts",
                    "presence_sub_menu": false,
                    "actual_plural_label": "Accounts",
                    "lookupable": false,
                    "id": "738692000000000045",
                    "isBlueprintSupported": false,
                    "visibility": 1,
                    "convertable": false,
                    "sub_menu_available": true,
                    "editable": true,
                    "actual_singular_label": "Account",
                    "profiles":
                    [
                        {
                            "name": "Administrator",
                            "id": "738692000000026972"
                        },
                        {
                            "name": "Standard",
                            "id": "738692000000026974"
                        }
                    ],
                    "show_as_tab": true,
                    "web_link": null,
                    "sequence_number": 4,
                    "singular_label": "Account",
                    "viewable": true,
                    "api_supported": true,
                    "api_name": "Accounts",
                    "quick_create": false,
                    "modified_by":
                    {
                        "name": "Daniel García",
                        "id": "738692000000414001"
                    },
                    "generated_type": "default",
                    "feeds_required": false,
                    "public_fields_configured": false,
                    "arguments":
                    [],
                    "module_name": "Accounts",
                    "profile_count": 2,
                    "business_card_field_limit": 5,
                    "parent_module":
                    {},
                    "status": "user_hidden"
                },
                {
                    "has_more_profiles": false,
                    "access_type": "org_based",
                    "private_profile": null,
                    "global_search_supported": true,
                    "deletable": true,
                    "description": null,
                    "creatable": true,
                    "recycle_bin_on_delete": true,
                    "modified_time": "2024-11-05T17:56:25+01:00",
                    "plural_label": "Products",
                    "presence_sub_menu": true,
                    "actual_plural_label": "Products",
                    "lookupable": true,
                    "id": "738692000000000099",
                    "isBlueprintSupported": true,
                    "visibility": 1,
                    "convertable": false,
                    "sub_menu_available": true,
                    "editable": true,
                    "actual_singular_label": "Product",
                    "profiles":
                    [
                        {
                            "name": "Administrator",
                            "id": "738692000000026972"
                        },
                        {
                            "name": "Standard",
                            "id": "738692000000026974"
                        }
                    ],
                    "show_as_tab": true,
                    "web_link": null,
                    "sequence_number": 4,
                    "singular_label": "Product",
                    "viewable": true,
                    "api_supported": true,
                    "api_name": "Products",
                    "quick_create": true,
                    "modified_by":
                    {
                        "name": "Daniel García",
                        "id": "738692000000414001"
                    },
                    "generated_type": "default",
                    "feeds_required": false,
                    "public_fields_configured": false,
                    "arguments":
                    [],
                    "module_name": "Products",
                    "profile_count": 2,
                    "business_card_field_limit": 5,
                    "parent_module":
                    {},
                    "status": "visible"
                },
                {
                    "has_more_profiles": false,
                    "access_type": "org_based",
                    "private_profile": null,
                    "global_search_supported": true,
                    "deletable": true,
                    "description": null,
                    "creatable": true,
                    "recycle_bin_on_delete": true,
                    "modified_time": "2024-10-09T16:26:27+02:00",
                    "plural_label": "Purchase Orders",
                    "presence_sub_menu": true,
                    "actual_plural_label": "Purchase Orders",
                    "lookupable": true,
                    "id": "738692000000000109",
                    "isBlueprintSupported": true,
                    "visibility": 1,
                    "convertable": false,
                    "sub_menu_available": true,
                    "editable": true,
                    "actual_singular_label": "Purchase Order",
                    "profiles":
                    [
                        {
                            "name": "Administrator",
                            "id": "738692000000026972"
                        },
                        {
                            "name": "Standard",
                            "id": "738692000000026974"
                        }
                    ],
                    "show_as_tab": true,
                    "web_link": null,
                    "sequence_number": 5,
                    "singular_label": "Purchase Order",
                    "viewable": true,
                    "api_supported": true,
                    "api_name": "Purchase_Orders",
                    "quick_create": true,
                    "modified_by":
                    {
                        "name": "Daniel García",
                        "id": "738692000000414001"
                    },
                    "generated_type": "default",
                    "feeds_required": false,
                    "public_fields_configured": false,
                    "arguments":
                    [],
                    "module_name": "PurchaseOrders",
                    "profile_count": 2,
                    "business_card_field_limit": 5,
                    "parent_module":
                    {},
                    "status": "visible"
                },
                {
                    "has_more_profiles": false,
                    "access_type": "org_based",
                    "private_profile": null,
                    "global_search_supported": true,
                    "deletable": true,
                    "description": null,
                    "creatable": true,
                    "recycle_bin_on_delete": true,
                    "modified_time": "2024-11-05T17:05:25+01:00",
                    "plural_label": "Course Progress",
                    "presence_sub_menu": true,
                    "actual_plural_label": "Course Progress",
                    "lookupable": true,
                    "id": "738692000001239168",
                    "isBlueprintSupported": true,
                    "visibility": 1,
                    "convertable": false,
                    "sub_menu_available": true,
                    "editable": true,
                    "actual_singular_label": "Course Progress",
                    "profiles":
                    [
                        {
                            "name": "Administrator",
                            "id": "738692000000026972"
                        }
                    ],
                    "show_as_tab": true,
                    "web_link": null,
                    "sequence_number": 6,
                    "singular_label": "Course Progress",
                    "viewable": true,
                    "api_supported": true,
                    "api_name": "Course_Progress",
                    "quick_create": true,
                    "modified_by":
                    {
                        "name": "Daniel García",
                        "id": "738692000000414001"
                    },
                    "generated_type": "custom",
                    "feeds_required": false,
                    "public_fields_configured": false,
                    "arguments":
                    [],
                    "module_name": "CustomModule1",
                    "profile_count": 1,
                    "business_card_field_limit": 5,
                    "parent_module":
                    {},
                    "status": "visible"
                },
                {
                    "has_more_profiles": false,
                    "access_type": "org_based",
                    "private_profile": null,
                    "global_search_supported": true,
                    "deletable": true,
                    "description": null,
                    "creatable": true,
                    "recycle_bin_on_delete": true,
                    "modified_time": null,
                    "plural_label": "Quotes",
                    "presence_sub_menu": true,
                    "actual_plural_label": "Quotes",
                    "lookupable": true,
                    "id": "738692000000000105",
                    "isBlueprintSupported": true,
                    "visibility": 1,
                    "convertable": true,
                    "sub_menu_available": true,
                    "editable": true,
                    "actual_singular_label": "Quote",
                    "profiles":
                    [
                        {
                            "name": "Administrator",
                            "id": "738692000000026972"
                        },
                        {
                            "name": "Standard",
                            "id": "738692000000026974"
                        }
                    ],
                    "show_as_tab": true,
                    "web_link": null,
                    "sequence_number": 7,
                    "singular_label": "Quote",
                    "viewable": true,
                    "api_supported": true,
                    "api_name": "Quotes",
                    "quick_create": true,
                    "modified_by": null,
                    "generated_type": "default",
                    "feeds_required": false,
                    "public_fields_configured": false,
                    "arguments":
                    [],
                    "module_name": "Quotes",
                    "profile_count": 2,
                    "business_card_field_limit": 5,
                    "parent_module":
                    {},
                    "status": "visible"
                },
                {
                    "has_more_profiles": false,
                    "access_type": "org_based",
                    "private_profile": null,
                    "global_search_supported": false,
                    "deletable": false,
                    "description": null,
                    "creatable": false,
                    "recycle_bin_on_delete": false,
                    "modified_time": "2024-09-27T14:48:14+02:00",
                    "plural_label": "Reports",
                    "presence_sub_menu": false,
                    "actual_plural_label": "Reports",
                    "lookupable": false,
                    "id": "738692000000000053",
                    "isBlueprintSupported": false,
                    "visibility": 1,
                    "convertable": false,
                    "sub_menu_available": false,
                    "editable": false,
                    "actual_singular_label": "Report",
                    "profiles":
                    [
                        {
                            "name": "Administrator",
                            "id": "738692000000026972"
                        },
                        {
                            "name": "Standard",
                            "id": "738692000000026974"
                        }
                    ],
                    "show_as_tab": true,
                    "web_link": null,
                    "sequence_number": 8,
                    "singular_label": "Report",
                    "viewable": true,
                    "api_supported": false,
                    "api_name": "Reports",
                    "quick_create": false,
                    "modified_by":
                    {
                        "name": "Daniel García",
                        "id": "738692000000414001"
                    },
                    "generated_type": "default",
                    "feeds_required": false,
                    "public_fields_configured": false,
                    "arguments":
                    [],
                    "module_name": "Reports",
                    "profile_count": 2,
                    "business_card_field_limit": 5,
                    "parent_module":
                    {},
                    "status": "user_hidden"
                },
                {
                    "has_more_profiles": false,
                    "access_type": "org_based",
                    "private_profile": null,
                    "global_search_supported": true,
                    "deletable": true,
                    "description": null,
                    "creatable": true,
                    "recycle_bin_on_delete": true,
                    "modified_time": null,
                    "plural_label": "Invoices",
                    "presence_sub_menu": true,
                    "actual_plural_label": "Invoices",
                    "lookupable": true,
                    "id": "738692000000000111",
                    "isBlueprintSupported": true,
                    "visibility": 1,
                    "convertable": false,
                    "sub_menu_available": true,
                    "editable": true,
                    "actual_singular_label": "Invoice",
                    "profiles":
                    [
                        {
                            "name": "Administrator",
                            "id": "738692000000026972"
                        },
                        {
                            "name": "Standard",
                            "id": "738692000000026974"
                        }
                    ],
                    "show_as_tab": true,
                    "web_link": null,
                    "sequence_number": 8,
                    "singular_label": "Invoice",
                    "viewable": true,
                    "api_supported": true,
                    "api_name": "Invoices",
                    "quick_create": true,
                    "modified_by": null,
                    "generated_type": "default",
                    "feeds_required": false,
                    "public_fields_configured": false,
                    "arguments":
                    [],
                    "module_name": "Invoices",
                    "profile_count": 2,
                    "business_card_field_limit": 5,
                    "parent_module":
                    {},
                    "status": "visible"
                },
                {
                    "has_more_profiles": false,
                    "access_type": "org_based",
                    "private_profile": null,
                    "global_search_supported": false,
                    "deletable": false,
                    "description": null,
                    "creatable": false,
                    "recycle_bin_on_delete": false,
                    "modified_time": null,
                    "plural_label": "My Jobs",
                    "presence_sub_menu": false,
                    "actual_plural_label": "My Jobs",
                    "lookupable": false,
                    "id": "738692000000000089",
                    "isBlueprintSupported": false,
                    "visibility": 1,
                    "convertable": false,
                    "sub_menu_available": false,
                    "editable": false,
                    "actual_singular_label": "Approvals",
                    "profiles":
                    [
                        {
                            "name": "Administrator",
                            "id": "738692000000026972"
                        },
                        {
                            "name": "Standard",
                            "id": "738692000000026974"
                        }
                    ],
                    "show_as_tab": false,
                    "web_link": null,
                    "sequence_number": 9,
                    "singular_label": "Approvals",
                    "viewable": true,
                    "api_supported": true,
                    "api_name": "Approvals",
                    "quick_create": false,
                    "modified_by": null,
                    "generated_type": "default",
                    "feeds_required": false,
                    "public_fields_configured": false,
                    "arguments":
                    [],
                    "module_name": "Approvals",
                    "profile_count": 2,
                    "business_card_field_limit": 5,
                    "parent_module":
                    {},
                    "status": "visible"
                },
                {
                    "has_more_profiles": false,
                    "access_type": "org_based",
                    "private_profile": null,
                    "global_search_supported": true,
                    "deletable": true,
                    "description": null,
                    "creatable": true,
                    "recycle_bin_on_delete": true,
                    "modified_time": null,
                    "plural_label": "Meetings",
                    "presence_sub_menu": true,
                    "actual_plural_label": "Meetings",
                    "lookupable": false,
                    "id": "738692000000000065",
                    "isBlueprintSupported": true,
                    "visibility": 1,
                    "convertable": false,
                    "sub_menu_available": true,
                    "editable": true,
                    "actual_singular_label": "Meeting",
                    "profiles":
                    [
                        {
                            "name": "Administrator",
                            "id": "738692000000026972"
                        },
                        {
                            "name": "Standard",
                            "id": "738692000000026974"
                        }
                    ],
                    "show_as_tab": true,
                    "web_link": null,
                    "sequence_number": 10,
                    "singular_label": "Meeting",
                    "viewable": true,
                    "api_supported": true,
                    "api_name": "Events",
                    "quick_create": true,
                    "modified_by": null,
                    "generated_type": "default",
                    "feeds_required": false,
                    "public_fields_configured": false,
                    "arguments":
                    [],
                    "module_name": "Meetings",
                    "profile_count": 2,
                    "business_card_field_limit": 5,
                    "parent_module":
                    {},
                    "status": "visible"
                },
                {
                    "has_more_profiles": false,
                    "access_type": "org_based",
                    "private_profile": null,
                    "global_search_supported": true,
                    "deletable": true,
                    "description": null,
                    "creatable": true,
                    "recycle_bin_on_delete": true,
                    "modified_time": null,
                    "plural_label": "Calls",
                    "presence_sub_menu": true,
                    "actual_plural_label": "Calls",
                    "lookupable": false,
                    "id": "738692000000000067",
                    "isBlueprintSupported": false,
                    "visibility": 1,
                    "convertable": false,
                    "sub_menu_available": true,
                    "editable": true,
                    "actual_singular_label": "Call",
                    "profiles":
                    [
                        {
                            "name": "Administrator",
                            "id": "738692000000026972"
                        },
                        {
                            "name": "Standard",
                            "id": "738692000000026974"
                        }
                    ],
                    "show_as_tab": true,
                    "web_link": null,
                    "sequence_number": 11,
                    "singular_label": "Call",
                    "viewable": true,
                    "api_supported": true,
                    "api_name": "Calls",
                    "quick_create": true,
                    "modified_by": null,
                    "generated_type": "default",
                    "feeds_required": false,
                    "public_fields_configured": false,
                    "arguments":
                    [],
                    "module_name": "Calls",
                    "profile_count": 2,
                    "business_card_field_limit": 5,
                    "parent_module":
                    {},
                    "status": "visible"
                },
                {
                    "has_more_profiles": false,
                    "access_type": "org_based",
                    "private_profile": null,
                    "global_search_supported": true,
                    "deletable": true,
                    "description": null,
                    "creatable": true,
                    "recycle_bin_on_delete": true,
                    "modified_time": null,
                    "plural_label": "Deals",
                    "presence_sub_menu": true,
                    "actual_plural_label": "Deals",
                    "lookupable": true,
                    "id": "738692000000000049",
                    "isBlueprintSupported": true,
                    "visibility": 1,
                    "convertable": false,
                    "sub_menu_available": true,
                    "editable": true,
                    "actual_singular_label": "Deal",
                    "profiles":
                    [
                        {
                            "name": "Administrator",
                            "id": "738692000000026972"
                        },
                        {
                            "name": "Standard",
                            "id": "738692000000026974"
                        }
                    ],
                    "show_as_tab": true,
                    "web_link": null,
                    "sequence_number": 12,
                    "singular_label": "Deal",
                    "viewable": true,
                    "api_supported": true,
                    "api_name": "Deals",
                    "quick_create": true,
                    "modified_by": null,
                    "generated_type": "default",
                    "feeds_required": true,
                    "public_fields_configured": false,
                    "arguments":
                    [],
                    "module_name": "Deals",
                    "profile_count": 2,
                    "business_card_field_limit": 5,
                    "parent_module":
                    {},
                    "status": "visible"
                },
                {
                    "has_more_profiles": false,
                    "access_type": "org_based",
                    "private_profile": null,
                    "global_search_supported": true,
                    "deletable": true,
                    "description": null,
                    "creatable": true,
                    "recycle_bin_on_delete": true,
                    "modified_time": "2024-10-09T09:45:45+02:00",
                    "plural_label": "Sales Orders",
                    "presence_sub_menu": true,
                    "actual_plural_label": "Sales Orders",
                    "lookupable": true,
                    "id": "738692000000000107",
                    "isBlueprintSupported": true,
                    "visibility": 1,
                    "convertable": true,
                    "sub_menu_available": true,
                    "editable": true,
                    "actual_singular_label": "Sales Order",
                    "profiles":
                    [
                        {
                            "name": "Administrator",
                            "id": "738692000000026972"
                        },
                        {
                            "name": "Standard",
                            "id": "738692000000026974"
                        }
                    ],
                    "show_as_tab": true,
                    "web_link": null,
                    "sequence_number": 13,
                    "singular_label": "Sales Order",
                    "viewable": true,
                    "api_supported": true,
                    "api_name": "Sales_Orders",
                    "quick_create": true,
                    "modified_by":
                    {
                        "name": "Daniel García",
                        "id": "738692000000414001"
                    },
                    "generated_type": "default",
                    "feeds_required": false,
                    "public_fields_configured": false,
                    "arguments":
                    [],
                    "module_name": "SalesOrders",
                    "profile_count": 2,
                    "business_card_field_limit": 5,
                    "parent_module":
                    {},
                    "status": "visible"
                },
                {
                    "has_more_profiles": false,
                    "access_type": "org_based",
                    "private_profile": null,
                    "global_search_supported": true,
                    "deletable": true,
                    "description": null,
                    "creatable": true,
                    "recycle_bin_on_delete": true,
                    "modified_time": null,
                    "plural_label": "Tasks",
                    "presence_sub_menu": true,
                    "actual_plural_label": "Tasks",
                    "lookupable": false,
                    "id": "738692000000000063",
                    "isBlueprintSupported": true,
                    "visibility": 1,
                    "convertable": false,
                    "sub_menu_available": true,
                    "editable": true,
                    "actual_singular_label": "Task",
                    "profiles":
                    [
                        {
                            "name": "Administrator",
                            "id": "738692000000026972"
                        },
                        {
                            "name": "Standard",
                            "id": "738692000000026974"
                        }
                    ],
                    "show_as_tab": true,
                    "web_link": null,
                    "sequence_number": 14,
                    "singular_label": "Task",
                    "viewable": true,
                    "api_supported": true,
                    "api_name": "Tasks",
                    "quick_create": true,
                    "modified_by": null,
                    "generated_type": "default",
                    "feeds_required": false,
                    "public_fields_configured": false,
                    "arguments":
                    [],
                    "module_name": "Tasks",
                    "profile_count": 2,
                    "business_card_field_limit": 5,
                    "parent_module":
                    {},
                    "status": "visible"
                },
                {
                    "has_more_profiles": false,
                    "access_type": "org_based",
                    "private_profile": null,
                    "global_search_supported": false,
                    "deletable": false,
                    "description": null,
                    "creatable": false,
                    "recycle_bin_on_delete": false,
                    "modified_time": "2024-09-27T14:46:48+02:00",
                    "plural_label": "SalesInbox",
                    "presence_sub_menu": false,
                    "actual_plural_label": "SalesInbox",
                    "lookupable": false,
                    "id": "738692000000062001",
                    "isBlueprintSupported": false,
                    "visibility": 1,
                    "convertable": false,
                    "sub_menu_available": false,
                    "editable": false,
                    "actual_singular_label": "SalesInbox",
                    "profiles":
                    [
                        {
                            "name": "Administrator",
                            "id": "738692000000026972"
                        },
                        {
                            "name": "Standard",
                            "id": "738692000000026974"
                        }
                    ],
                    "show_as_tab": true,
                    "web_link": null,
                    "sequence_number": 14,
                    "singular_label": "SalesInbox",
                    "viewable": true,
                    "api_supported": false,
                    "api_name": "SalesInbox",
                    "quick_create": false,
                    "modified_by":
                    {
                        "name": "Daniel García",
                        "id": "738692000000414001"
                    },
                    "generated_type": "default",
                    "feeds_required": false,
                    "public_fields_configured": false,
                    "arguments":
                    [],
                    "module_name": "SalesInbox",
                    "profile_count": 2,
                    "business_card_field_limit": 5,
                    "parent_module":
                    {},
                    "status": "user_hidden"
                },
                {
                    "has_more_profiles": false,
                    "access_type": "org_based",
                    "private_profile": null,
                    "global_search_supported": false,
                    "deletable": false,
                    "description": null,
                    "creatable": false,
                    "recycle_bin_on_delete": false,
                    "modified_time": "2024-10-08T14:57:50+02:00",
                    "plural_label": "Analytics",
                    "presence_sub_menu": false,
                    "actual_plural_label": "Analytics",
                    "lookupable": false,
                    "id": "738692000000000055",
                    "isBlueprintSupported": false,
                    "visibility": 1,
                    "convertable": false,
                    "sub_menu_available": false,
                    "editable": false,
                    "actual_singular_label": "Analytics",
                    "profiles":
                    [
                        {
                            "name": "Administrator",
                            "id": "738692000000026972"
                        },
                        {
                            "name": "Standard",
                            "id": "738692000000026974"
                        }
                    ],
                    "show_as_tab": true,
                    "web_link": null,
                    "sequence_number": 15,
                    "singular_label": "Analytics",
                    "viewable": true,
                    "api_supported": false,
                    "api_name": "Analytics",
                    "quick_create": false,
                    "modified_by":
                    {
                        "name": "Daniel García",
                        "id": "738692000000414001"
                    },
                    "generated_type": "default",
                    "feeds_required": false,
                    "public_fields_configured": false,
                    "arguments":
                    [],
                    "module_name": "Dashboards",
                    "profile_count": 2,
                    "business_card_field_limit": 5,
                    "parent_module":
                    {},
                    "status": "visible"
                },
                {
                    "has_more_profiles": false,
                    "access_type": "org_based",
                    "private_profile": null,
                    "global_search_supported": false,
                    "deletable": false,
                    "description": null,
                    "creatable": false,
                    "recycle_bin_on_delete": false,
                    "modified_time": "2024-10-08T14:57:50+02:00",
                    "plural_label": "Feeds",
                    "presence_sub_menu": false,
                    "actual_plural_label": "Feeds",
                    "lookupable": false,
                    "id": "738692000000000083",
                    "isBlueprintSupported": false,
                    "visibility": 1,
                    "convertable": false,
                    "sub_menu_available": false,
                    "editable": false,
                    "actual_singular_label": "Feeds",
                    "profiles":
                    [
                        {
                            "name": "Administrator",
                            "id": "738692000000026972"
                        },
                        {
                            "name": "Standard",
                            "id": "738692000000026974"
                        }
                    ],
                    "show_as_tab": true,
                    "web_link": null,
                    "sequence_number": 16,
                    "singular_label": "Feeds",
                    "viewable": true,
                    "api_supported": false,
                    "api_name": "Feeds",
                    "quick_create": false,
                    "modified_by":
                    {
                        "name": "Daniel García",
                        "id": "738692000000414001"
                    },
                    "generated_type": "default",
                    "feeds_required": false,
                    "public_fields_configured": false,
                    "arguments":
                    [],
                    "module_name": "Feeds",
                    "profile_count": 2,
                    "business_card_field_limit": 5,
                    "parent_module":
                    {},
                    "status": "visible"
                },
                {
                    "has_more_profiles": false,
                    "access_type": "org_based",
                    "private_profile": null,
                    "global_search_supported": true,
                    "deletable": true,
                    "description": null,
                    "creatable": true,
                    "recycle_bin_on_delete": true,
                    "modified_time": "2024-10-08T14:57:50+02:00",
                    "plural_label": "Campaigns",
                    "presence_sub_menu": true,
                    "actual_plural_label": "Campaigns",
                    "lookupable": true,
                    "id": "738692000000000051",
                    "isBlueprintSupported": true,
                    "visibility": 1,
                    "convertable": false,
                    "sub_menu_available": true,
                    "editable": true,
                    "actual_singular_label": "Campaign",
                    "profiles":
                    [
                        {
                            "name": "Administrator",
                            "id": "738692000000026972"
                        },
                        {
                            "name": "Standard",
                            "id": "738692000000026974"
                        }
                    ],
                    "show_as_tab": true,
                    "web_link": null,
                    "sequence_number": 17,
                    "singular_label": "Campaign",
                    "viewable": true,
                    "api_supported": true,
                    "api_name": "Campaigns",
                    "quick_create": true,
                    "modified_by":
                    {
                        "name": "Daniel García",
                        "id": "738692000000414001"
                    },
                    "generated_type": "default",
                    "feeds_required": false,
                    "public_fields_configured": false,
                    "arguments":
                    [],
                    "module_name": "Campaigns",
                    "profile_count": 2,
                    "business_card_field_limit": 5,
                    "parent_module":
                    {},
                    "status": "visible"
                },
                {
                    "has_more_profiles": false,
                    "access_type": "org_based",
                    "private_profile": null,
                    "global_search_supported": true,
                    "deletable": true,
                    "description": null,
                    "creatable": true,
                    "recycle_bin_on_delete": true,
                    "modified_time": "2024-09-27T14:46:48+02:00",
                    "plural_label": "Vendors",
                    "presence_sub_menu": false,
                    "actual_plural_label": "Vendors",
                    "lookupable": false,
                    "id": "738692000000000101",
                    "isBlueprintSupported": false,
                    "visibility": 1,
                    "convertable": false,
                    "sub_menu_available": true,
                    "editable": true,
                    "actual_singular_label": "Vendor",
                    "profiles":
                    [
                        {
                            "name": "Administrator",
                            "id": "738692000000026972"
                        },
                        {
                            "name": "Standard",
                            "id": "738692000000026974"
                        }
                    ],
                    "show_as_tab": true,
                    "web_link": null,
                    "sequence_number": 17,
                    "singular_label": "Vendor",
                    "viewable": true,
                    "api_supported": true,
                    "api_name": "Vendors",
                    "quick_create": false,
                    "modified_by":
                    {
                        "name": "Daniel García",
                        "id": "738692000000414001"
                    },
                    "generated_type": "default",
                    "feeds_required": false,
                    "public_fields_configured": false,
                    "arguments":
                    [],
                    "module_name": "Vendors",
                    "profile_count": 2,
                    "business_card_field_limit": 5,
                    "parent_module":
                    {},
                    "status": "user_hidden"
                },
                {
                    "has_more_profiles": false,
                    "access_type": "org_based",
                    "private_profile": null,
                    "global_search_supported": false,
                    "deletable": false,
                    "description": null,
                    "creatable": false,
                    "recycle_bin_on_delete": false,
                    "modified_time": "2024-10-08T14:57:50+02:00",
                    "plural_label": "Visits",
                    "presence_sub_menu": true,
                    "actual_plural_label": "Visits",
                    "lookupable": false,
                    "id": "738692000000000093",
                    "isBlueprintSupported": false,
                    "visibility": 1,
                    "convertable": false,
                    "sub_menu_available": true,
                    "editable": false,
                    "actual_singular_label": "Visit",
                    "profiles":
                    [
                        {
                            "name": "Administrator",
                            "id": "738692000000026972"
                        }
                    ],
                    "show_as_tab": true,
                    "web_link": null,
                    "sequence_number": 18,
                    "singular_label": "Visit",
                    "viewable": true,
                    "api_supported": true,
                    "api_name": "Visits",
                    "quick_create": false,
                    "modified_by":
                    {
                        "name": "Daniel García",
                        "id": "738692000000414001"
                    },
                    "generated_type": "default",
                    "feeds_required": false,
                    "public_fields_configured": false,
                    "arguments":
                    [],
                    "module_name": "Visits",
                    "profile_count": 1,
                    "business_card_field_limit": 5,
                    "parent_module":
                    {},
                    "status": "visible"
                },
                {
                    "has_more_profiles": false,
                    "access_type": "org_based",
                    "private_profile": null,
                    "global_search_supported": true,
                    "deletable": true,
                    "description": null,
                    "creatable": true,
                    "recycle_bin_on_delete": true,
                    "modified_time": "2024-09-27T14:46:48+02:00",
                    "plural_label": "Price Books",
                    "presence_sub_menu": false,
                    "actual_plural_label": "Price Books",
                    "lookupable": false,
                    "id": "738692000000000103",
                    "isBlueprintSupported": false,
                    "visibility": 1,
                    "convertable": false,
                    "sub_menu_available": true,
                    "editable": true,
                    "actual_singular_label": "Price Book",
                    "profiles":
                    [
                        {
                            "name": "Administrator",
                            "id": "738692000000026972"
                        },
                        {
                            "name": "Standard",
                            "id": "738692000000026974"
                        }
                    ],
                    "show_as_tab": true,
                    "web_link": null,
                    "sequence_number": 18,
                    "singular_label": "Price Book",
                    "viewable": true,
                    "api_supported": true,
                    "api_name": "Price_Books",
                    "quick_create": false,
                    "modified_by":
                    {
                        "name": "Daniel García",
                        "id": "738692000000414001"
                    },
                    "generated_type": "default",
                    "feeds_required": false,
                    "public_fields_configured": false,
                    "arguments":
                    [],
                    "module_name": "PriceBooks",
                    "profile_count": 2,
                    "business_card_field_limit": 5,
                    "parent_module":
                    {},
                    "status": "user_hidden"
                },
                {
                    "has_more_profiles": false,
                    "access_type": "org_based",
                    "private_profile": null,
                    "global_search_supported": false,
                    "deletable": false,
                    "description": null,
                    "creatable": false,
                    "recycle_bin_on_delete": false,
                    "modified_time": "2024-10-08T14:57:50+02:00",
                    "plural_label": "Social",
                    "presence_sub_menu": false,
                    "actual_plural_label": "Social",
                    "lookupable": false,
                    "id": "738692000000000091",
                    "isBlueprintSupported": false,
                    "visibility": 1,
                    "convertable": false,
                    "sub_menu_available": false,
                    "editable": false,
                    "actual_singular_label": "Social",
                    "profiles":
                    [
                        {
                            "name": "Administrator",
                            "id": "738692000000026972"
                        }
                    ],
                    "show_as_tab": true,
                    "web_link": null,
                    "sequence_number": 19,
                    "singular_label": "Social",
                    "viewable": true,
                    "api_supported": false,
                    "api_name": "Social",
                    "quick_create": false,
                    "modified_by":
                    {
                        "name": "Daniel García",
                        "id": "738692000000414001"
                    },
                    "generated_type": "default",
                    "feeds_required": false,
                    "public_fields_configured": false,
                    "arguments":
                    [],
                    "module_name": "Social",
                    "profile_count": 1,
                    "business_card_field_limit": 5,
                    "parent_module":
                    {},
                    "status": "visible"
                },
                {
                    "has_more_profiles": false,
                    "access_type": "org_based",
                    "private_profile": null,
                    "global_search_supported": true,
                    "deletable": true,
                    "description": null,
                    "creatable": true,
                    "recycle_bin_on_delete": true,
                    "modified_time": "2024-09-27T14:46:48+02:00",
                    "plural_label": "Cases",
                    "presence_sub_menu": false,
                    "actual_plural_label": "Cases",
                    "lookupable": false,
                    "id": "738692000000000095",
                    "isBlueprintSupported": false,
                    "visibility": 1,
                    "convertable": false,
                    "sub_menu_available": true,
                    "editable": true,
                    "actual_singular_label": "Case",
                    "profiles":
                    [
                        {
                            "name": "Administrator",
                            "id": "738692000000026972"
                        },
                        {
                            "name": "Standard",
                            "id": "738692000000026974"
                        }
                    ],
                    "show_as_tab": true,
                    "web_link": null,
                    "sequence_number": 19,
                    "singular_label": "Case",
                    "viewable": true,
                    "api_supported": true,
                    "api_name": "Cases",
                    "quick_create": false,
                    "modified_by":
                    {
                        "name": "Daniel García",
                        "id": "738692000000414001"
                    },
                    "generated_type": "default",
                    "feeds_required": false,
                    "public_fields_configured": false,
                    "arguments":
                    [],
                    "module_name": "Cases",
                    "profile_count": 2,
                    "business_card_field_limit": 5,
                    "parent_module":
                    {},
                    "status": "user_hidden"
                },
                {
                    "has_more_profiles": false,
                    "access_type": "org_based",
                    "private_profile": null,
                    "global_search_supported": true,
                    "deletable": true,
                    "description": null,
                    "creatable": true,
                    "recycle_bin_on_delete": true,
                    "modified_time": "2024-09-27T14:46:48+02:00",
                    "plural_label": "Solutions",
                    "presence_sub_menu": false,
                    "actual_plural_label": "Solutions",
                    "lookupable": false,
                    "id": "738692000000000097",
                    "isBlueprintSupported": false,
                    "visibility": 1,
                    "convertable": false,
                    "sub_menu_available": true,
                    "editable": true,
                    "actual_singular_label": "Solution",
                    "profiles":
                    [
                        {
                            "name": "Administrator",
                            "id": "738692000000026972"
                        },
                        {
                            "name": "Standard",
                            "id": "738692000000026974"
                        }
                    ],
                    "show_as_tab": true,
                    "web_link": null,
                    "sequence_number": 20,
                    "singular_label": "Solution",
                    "viewable": true,
                    "api_supported": true,
                    "api_name": "Solutions",
                    "quick_create": false,
                    "modified_by":
                    {
                        "name": "Daniel García",
                        "id": "738692000000414001"
                    },
                    "generated_type": "default",
                    "feeds_required": false,
                    "public_fields_configured": false,
                    "arguments":
                    [],
                    "module_name": "Solutions",
                    "profile_count": 2,
                    "business_card_field_limit": 5,
                    "parent_module":
                    {},
                    "status": "user_hidden"
                },
                {
                    "has_more_profiles": false,
                    "access_type": "org_based",
                    "private_profile": null,
                    "global_search_supported": false,
                    "deletable": false,
                    "description": null,
                    "creatable": false,
                    "recycle_bin_on_delete": false,
                    "modified_time": "2024-09-27T14:46:48+02:00",
                    "plural_label": "Documents",
                    "presence_sub_menu": false,
                    "actual_plural_label": "Documents",
                    "lookupable": false,
                    "id": "738692000000000087",
                    "isBlueprintSupported": false,
                    "visibility": 1,
                    "convertable": false,
                    "sub_menu_available": false,
                    "editable": false,
                    "actual_singular_label": "Documents",
                    "profiles":
                    [
                        {
                            "name": "Administrator",
                            "id": "738692000000026972"
                        },
                        {
                            "name": "Standard",
                            "id": "738692000000026974"
                        }
                    ],
                    "show_as_tab": true,
                    "web_link": null,
                    "sequence_number": 21,
                    "singular_label": "Documents",
                    "viewable": true,
                    "api_supported": false,
                    "api_name": "Documents",
                    "quick_create": false,
                    "modified_by":
                    {
                        "name": "Daniel García",
                        "id": "738692000000414001"
                    },
                    "generated_type": "default",
                    "feeds_required": false,
                    "public_fields_configured": false,
                    "arguments":
                    [],
                    "module_name": "Documents",
                    "profile_count": 2,
                    "business_card_field_limit": 5,
                    "parent_module":
                    {},
                    "status": "user_hidden"
                },
                {
                    "has_more_profiles": false,
                    "access_type": "org_based",
                    "private_profile": null,
                    "global_search_supported": false,
                    "deletable": false,
                    "description": null,
                    "creatable": false,
                    "recycle_bin_on_delete": false,
                    "modified_time": "2024-09-27T14:46:48+02:00",
                    "plural_label": "Forecasts",
                    "presence_sub_menu": false,
                    "actual_plural_label": "Forecasts",
                    "lookupable": false,
                    "id": "738692000000000073",
                    "isBlueprintSupported": false,
                    "visibility": 1,
                    "convertable": false,
                    "sub_menu_available": true,
                    "editable": false,
                    "actual_singular_label": "Forecast",
                    "profiles":
                    [
                        {
                            "name": "Administrator",
                            "id": "738692000000026972"
                        },
                        {
                            "name": "Standard",
                            "id": "738692000000026974"
                        }
                    ],
                    "show_as_tab": true,
                    "web_link": null,
                    "sequence_number": 22,
                    "singular_label": "Forecast",
                    "viewable": true,
                    "api_supported": false,
                    "api_name": "Forecasts",
                    "quick_create": false,
                    "modified_by":
                    {
                        "name": "Daniel García",
                        "id": "738692000000414001"
                    },
                    "generated_type": "default",
                    "feeds_required": false,
                    "public_fields_configured": false,
                    "arguments":
                    [],
                    "module_name": "Forecasts",
                    "profile_count": 2,
                    "business_card_field_limit": 5,
                    "parent_module":
                    {},
                    "status": "user_hidden"
                },
                {
                    "has_more_profiles": false,
                    "access_type": "org_based",
                    "private_profile": null,
                    "global_search_supported": false,
                    "deletable": true,
                    "description": null,
                    "creatable": true,
                    "recycle_bin_on_delete": true,
                    "modified_time": null,
                    "plural_label": "Invoiced Items",
                    "presence_sub_menu": false,
                    "actual_plural_label": "Invoiced Items",
                    "lookupable": false,
                    "id": "738692000000174001",
                    "isBlueprintSupported": false,
                    "visibility": 2,
                    "convertable": false,
                    "sub_menu_available": false,
                    "editable": true,
                    "actual_singular_label": "Invoiced Items",
                    "profiles":
                    [
                        {
                            "name": "Administrator",
                            "id": "738692000000026972"
                        },
                        {
                            "name": "Standard",
                            "id": "738692000000026974"
                        }
                    ],
                    "show_as_tab": false,
                    "web_link": null,
                    "sequence_number": 23,
                    "singular_label": "Invoiced Items",
                    "viewable": true,
                    "api_supported": true,
                    "api_name": "Invoiced_Items",
                    "quick_create": false,
                    "modified_by": null,
                    "generated_type": "subform",
                    "feeds_required": false,
                    "public_fields_configured": false,
                    "arguments":
                    [],
                    "module_name": "InvoicedItems",
                    "profile_count": 2,
                    "business_card_field_limit": 5,
                    "parent_module":
                    {
                        "api_name": "Invoices",
                        "id": "738692000000000111"
                    },
                    "status": "visible"
                },
                {
                    "has_more_profiles": false,
                    "access_type": "org_based",
                    "private_profile": null,
                    "global_search_supported": false,
                    "deletable": false,
                    "description": null,
                    "creatable": false,
                    "recycle_bin_on_delete": false,
                    "modified_time": null,
                    "plural_label": "EmailSentiment",
                    "presence_sub_menu": false,
                    "actual_plural_label": "EmailSentiment",
                    "lookupable": false,
                    "id": "738692000000139001",
                    "isBlueprintSupported": false,
                    "visibility": 2,
                    "convertable": false,
                    "sub_menu_available": false,
                    "editable": false,
                    "actual_singular_label": "EmailSentiment",
                    "profiles":
                    [
                        {
                            "name": "Administrator",
                            "id": "738692000000026972"
                        },
                        {
                            "name": "Standard",
                            "id": "738692000000026974"
                        }
                    ],
                    "show_as_tab": false,
                    "web_link": null,
                    "sequence_number": 24,
                    "singular_label": "EmailSentiment",
                    "viewable": false,
                    "api_supported": true,
                    "api_name": "Email_Sentiment",
                    "quick_create": false,
                    "modified_by": null,
                    "generated_type": "default",
                    "feeds_required": false,
                    "public_fields_configured": false,
                    "arguments":
                    [],
                    "module_name": "EmailSentiment",
                    "profile_count": 2,
                    "business_card_field_limit": 5,
                    "parent_module":
                    {},
                    "status": "visible"
                },
                {
                    "has_more_profiles": false,
                    "access_type": "org_based",
                    "private_profile": null,
                    "global_search_supported": false,
                    "deletable": true,
                    "description": null,
                    "creatable": true,
                    "recycle_bin_on_delete": true,
                    "modified_time": null,
                    "plural_label": "Purchase Items",
                    "presence_sub_menu": false,
                    "actual_plural_label": "Purchase Items",
                    "lookupable": false,
                    "id": "738692000000174419",
                    "isBlueprintSupported": false,
                    "visibility": 2,
                    "convertable": false,
                    "sub_menu_available": false,
                    "editable": true,
                    "actual_singular_label": "Purchase Items",
                    "profiles":
                    [
                        {
                            "name": "Administrator",
                            "id": "738692000000026972"
                        },
                        {
                            "name": "Standard",
                            "id": "738692000000026974"
                        }
                    ],
                    "show_as_tab": false,
                    "web_link": null,
                    "sequence_number": 24,
                    "singular_label": "Purchase Items",
                    "viewable": true,
                    "api_supported": true,
                    "api_name": "Purchase_Items",
                    "quick_create": false,
                    "modified_by": null,
                    "generated_type": "subform",
                    "feeds_required": false,
                    "public_fields_configured": false,
                    "arguments":
                    [],
                    "module_name": "PurchaseItems",
                    "profile_count": 2,
                    "business_card_field_limit": 5,
                    "parent_module":
                    {
                        "api_name": "Purchase_Orders",
                        "id": "738692000000000109"
                    },
                    "status": "visible"
                },
                {
                    "has_more_profiles": false,
                    "access_type": "org_based",
                    "private_profile": null,
                    "global_search_supported": false,
                    "deletable": false,
                    "description": null,
                    "creatable": false,
                    "recycle_bin_on_delete": false,
                    "modified_time": null,
                    "plural_label": "Email Analytics",
                    "presence_sub_menu": false,
                    "actual_plural_label": "Email Analytics",
                    "lookupable": false,
                    "id": "738692000000187017",
                    "isBlueprintSupported": false,
                    "visibility": 2,
                    "convertable": false,
                    "sub_menu_available": false,
                    "editable": false,
                    "actual_singular_label": "Email Analytics",
                    "profiles":
                    [
                        {
                            "name": "Administrator",
                            "id": "738692000000026972"
                        },
                        {
                            "name": "Standard",
                            "id": "738692000000026974"
                        }
                    ],
                    "show_as_tab": false,
                    "web_link": null,
                    "sequence_number": 24,
                    "singular_label": "Email Analytics",
                    "viewable": false,
                    "api_supported": true,
                    "api_name": "Email_Analytics",
                    "quick_create": false,
                    "modified_by": null,
                    "generated_type": "default",
                    "feeds_required": false,
                    "public_fields_configured": false,
                    "arguments":
                    [],
                    "module_name": "Email Analytics",
                    "profile_count": 2,
                    "business_card_field_limit": 5,
                    "parent_module":
                    {},
                    "status": "visible"
                },
                {
                    "has_more_profiles": false,
                    "access_type": "org_based",
                    "private_profile": null,
                    "global_search_supported": false,
                    "deletable": false,
                    "description": null,
                    "creatable": false,
                    "recycle_bin_on_delete": false,
                    "modified_time": null,
                    "plural_label": "Email Template Analytics",
                    "presence_sub_menu": false,
                    "actual_plural_label": "Email Template Analytics",
                    "lookupable": false,
                    "id": "738692000000187114",
                    "isBlueprintSupported": false,
                    "visibility": 2,
                    "convertable": false,
                    "sub_menu_available": false,
                    "editable": false,
                    "actual_singular_label": "Email Template Analytics",
                    "profiles":
                    [
                        {
                            "name": "Administrator",
                            "id": "738692000000026972"
                        },
                        {
                            "name": "Standard",
                            "id": "738692000000026974"
                        }
                    ],
                    "show_as_tab": false,
                    "web_link": null,
                    "sequence_number": 24,
                    "singular_label": "Email Template Analytics",
                    "viewable": false,
                    "api_supported": true,
                    "api_name": "Email_Template_Analytics",
                    "quick_create": false,
                    "modified_by": null,
                    "generated_type": "default",
                    "feeds_required": false,
                    "public_fields_configured": false,
                    "arguments":
                    [],
                    "module_name": "Email Template Analytics",
                    "profile_count": 2,
                    "business_card_field_limit": 5,
                    "parent_module":
                    {},
                    "status": "visible"
                },
                {
                    "has_more_profiles": false,
                    "access_type": "org_based",
                    "private_profile": null,
                    "global_search_supported": false,
                    "deletable": false,
                    "description": null,
                    "creatable": false,
                    "recycle_bin_on_delete": false,
                    "modified_time": "2024-09-27T14:46:48+02:00",
                    "plural_label": "Google Ads",
                    "presence_sub_menu": false,
                    "actual_plural_label": "Google AdWords",
                    "lookupable": false,
                    "id": "738692000000000057",
                    "isBlueprintSupported": false,
                    "visibility": 1,
                    "convertable": false,
                    "sub_menu_available": false,
                    "editable": false,
                    "actual_singular_label": "Google AdWords",
                    "profiles":
                    [
                        {
                            "name": "Administrator",
                            "id": "738692000000026972"
                        }
                    ],
                    "show_as_tab": false,
                    "web_link": null,
                    "sequence_number": 25,
                    "singular_label": "Google Ads",
                    "viewable": true,
                    "api_supported": false,
                    "api_name": "Google_AdWords",
                    "quick_create": false,
                    "modified_by":
                    {
                        "name": "Daniel García",
                        "id": "738692000000414001"
                    },
                    "generated_type": "default",
                    "feeds_required": false,
                    "public_fields_configured": false,
                    "arguments":
                    [],
                    "module_name": "Google AdWords",
                    "profile_count": 1,
                    "business_card_field_limit": 5,
                    "parent_module":
                    {},
                    "status": "user_hidden"
                },
                {
                    "has_more_profiles": false,
                    "access_type": "org_based",
                    "private_profile": null,
                    "global_search_supported": false,
                    "deletable": false,
                    "description": null,
                    "creatable": false,
                    "recycle_bin_on_delete": false,
                    "modified_time": null,
                    "track_current_data": true,
                    "plural_label": "Stage History",
                    "presence_sub_menu": false,
                    "actual_plural_label": "Stage History",
                    "lookupable": false,
                    "id": "738692000000113001",
                    "isBlueprintSupported": false,
                    "visibility": 2,
                    "convertable": false,
                    "sub_menu_available": false,
                    "editable": false,
                    "actual_singular_label": "Stage History",
                    "profiles":
                    [
                        {
                            "name": "Administrator",
                            "id": "738692000000026972"
                        },
                        {
                            "name": "Standard",
                            "id": "738692000000026974"
                        }
                    ],
                    "show_as_tab": false,
                    "web_link": null,
                    "sequence_number": 25,
                    "singular_label": "Stage History",
                    "viewable": true,
                    "api_supported": true,
                    "api_name": "DealHistory",
                    "quick_create": false,
                    "modified_by": null,
                    "generated_type": "field_tracker",
                    "feeds_required": false,
                    "public_fields_configured": false,
                    "arguments":
                    [],
                    "module_name": "DealHistory",
                    "profile_count": 2,
                    "business_card_field_limit": 5,
                    "parent_module":
                    {
                        "api_name": "Deals",
                        "id": "738692000000000049"
                    },
                    "status": "system_hidden"
                },
                {
                    "has_more_profiles": false,
                    "access_type": "org_based",
                    "private_profile": null,
                    "global_search_supported": false,
                    "deletable": true,
                    "description": null,
                    "creatable": true,
                    "recycle_bin_on_delete": true,
                    "modified_time": "2024-10-09T09:45:45+02:00",
                    "plural_label": "Productos",
                    "presence_sub_menu": false,
                    "actual_plural_label": "Productos",
                    "lookupable": false,
                    "id": "738692000000174837",
                    "isBlueprintSupported": false,
                    "visibility": 2,
                    "convertable": false,
                    "sub_menu_available": false,
                    "editable": true,
                    "actual_singular_label": "Productos",
                    "profiles":
                    [
                        {
                            "name": "Administrator",
                            "id": "738692000000026972"
                        },
                        {
                            "name": "Standard",
                            "id": "738692000000026974"
                        }
                    ],
                    "show_as_tab": false,
                    "web_link": null,
                    "sequence_number": 25,
                    "singular_label": "Productos",
                    "viewable": true,
                    "api_supported": true,
                    "api_name": "Ordered_Items",
                    "quick_create": false,
                    "modified_by":
                    {
                        "name": "Daniel García",
                        "id": "738692000000414001"
                    },
                    "generated_type": "subform",
                    "feeds_required": false,
                    "public_fields_configured": false,
                    "arguments":
                    [],
                    "module_name": "OrderedItems",
                    "profile_count": 2,
                    "business_card_field_limit": 5,
                    "parent_module":
                    {
                        "api_name": "Sales_Orders",
                        "id": "738692000000000107"
                    },
                    "status": "visible"
                },
                {
                    "has_more_profiles": false,
                    "access_type": "org_based",
                    "private_profile": null,
                    "global_search_supported": false,
                    "deletable": true,
                    "description": null,
                    "creatable": true,
                    "recycle_bin_on_delete": true,
                    "modified_time": null,
                    "plural_label": "Quoted Items",
                    "presence_sub_menu": false,
                    "actual_plural_label": "Quoted Items",
                    "lookupable": false,
                    "id": "738692000000175255",
                    "isBlueprintSupported": false,
                    "visibility": 2,
                    "convertable": false,
                    "sub_menu_available": false,
                    "editable": true,
                    "actual_singular_label": "Quoted Items",
                    "profiles":
                    [
                        {
                            "name": "Administrator",
                            "id": "738692000000026972"
                        },
                        {
                            "name": "Standard",
                            "id": "738692000000026974"
                        }
                    ],
                    "show_as_tab": false,
                    "web_link": null,
                    "sequence_number": 26,
                    "singular_label": "Quoted Items",
                    "viewable": true,
                    "api_supported": true,
                    "api_name": "Quoted_Items",
                    "quick_create": false,
                    "modified_by": null,
                    "generated_type": "subform",
                    "feeds_required": false,
                    "public_fields_configured": false,
                    "arguments":
                    [],
                    "module_name": "QuotedItems",
                    "profile_count": 2,
                    "business_card_field_limit": 5,
                    "parent_module":
                    {
                        "api_name": "Quotes",
                        "id": "738692000000000105"
                    },
                    "status": "visible"
                },
                {
                    "has_more_profiles": false,
                    "access_type": "org_based",
                    "private_profile": null,
                    "global_search_supported": true,
                    "deletable": true,
                    "description": null,
                    "creatable": true,
                    "recycle_bin_on_delete": true,
                    "modified_time": null,
                    "plural_label": "Notes",
                    "presence_sub_menu": false,
                    "actual_plural_label": "Notes",
                    "lookupable": false,
                    "id": "738692000000000069",
                    "isBlueprintSupported": false,
                    "visibility": 1,
                    "convertable": false,
                    "sub_menu_available": false,
                    "editable": true,
                    "actual_singular_label": "Note",
                    "profiles":
                    [
                        {
                            "name": "Administrator",
                            "id": "738692000000026972"
                        },
                        {
                            "name": "Standard",
                            "id": "738692000000026974"
                        }
                    ],
                    "show_as_tab": false,
                    "web_link": null,
                    "sequence_number": 31,
                    "singular_label": "Note",
                    "viewable": true,
                    "api_supported": true,
                    "api_name": "Notes",
                    "quick_create": false,
                    "modified_by": null,
                    "generated_type": "default",
                    "feeds_required": false,
                    "public_fields_configured": false,
                    "arguments":
                    [],
                    "module_name": "Notes",
                    "profile_count": 2,
                    "business_card_field_limit": 5,
                    "parent_module":
                    {},
                    "status": "system_hidden"
                },
                {
                    "has_more_profiles": false,
                    "access_type": "org_based",
                    "private_profile": null,
                    "global_search_supported": false,
                    "deletable": true,
                    "description": null,
                    "creatable": true,
                    "recycle_bin_on_delete": false,
                    "modified_time": null,
                    "plural_label": "Attachments",
                    "presence_sub_menu": false,
                    "actual_plural_label": "Attachments",
                    "lookupable": false,
                    "id": "738692000000000113",
                    "isBlueprintSupported": false,
                    "visibility": 1,
                    "convertable": false,
                    "sub_menu_available": false,
                    "editable": false,
                    "actual_singular_label": "Attachment",
                    "profiles":
                    [
                        {
                            "name": "Administrator",
                            "id": "738692000000026972"
                        },
                        {
                            "name": "Standard",
                            "id": "738692000000026974"
                        }
                    ],
                    "show_as_tab": false,
                    "web_link": null,
                    "sequence_number": 38,
                    "singular_label": "Attachment",
                    "viewable": true,
                    "api_supported": true,
                    "api_name": "Attachments",
                    "quick_create": false,
                    "modified_by": null,
                    "generated_type": "default",
                    "feeds_required": false,
                    "public_fields_configured": false,
                    "arguments":
                    [],
                    "module_name": "Attachments",
                    "profile_count": 2,
                    "business_card_field_limit": 5,
                    "parent_module":
                    {},
                    "status": "system_hidden"
                },
                {
                    "has_more_profiles": false,
                    "access_type": "org_based",
                    "private_profile": null,
                    "global_search_supported": false,
                    "deletable": false,
                    "description": null,
                    "creatable": false,
                    "recycle_bin_on_delete": false,
                    "modified_time": null,
                    "plural_label": "Emails",
                    "presence_sub_menu": false,
                    "actual_plural_label": "Emails",
                    "lookupable": false,
                    "id": "738692000000000115",
                    "isBlueprintSupported": false,
                    "visibility": 1,
                    "convertable": false,
                    "sub_menu_available": false,
                    "editable": false,
                    "actual_singular_label": "Email",
                    "profiles":
                    [
                        {
                            "name": "Administrator",
                            "id": "738692000000026972"
                        },
                        {
                            "name": "Standard",
                            "id": "738692000000026974"
                        }
                    ],
                    "show_as_tab": true,
                    "web_link": null,
                    "sequence_number": 39,
                    "singular_label": "Email",
                    "viewable": false,
                    "api_supported": false,
                    "api_name": "Emails",
                    "quick_create": false,
                    "modified_by": null,
                    "generated_type": "default",
                    "feeds_required": false,
                    "public_fields_configured": false,
                    "arguments":
                    [],
                    "module_name": "Emails",
                    "profile_count": 2,
                    "business_card_field_limit": 5,
                    "parent_module":
                    {},
                    "status": "visible"
                },
                {
                    "has_more_profiles": false,
                    "access_type": "org_based",
                    "private_profile": null,
                    "global_search_supported": false,
                    "deletable": false,
                    "description": null,
                    "creatable": false,
                    "recycle_bin_on_delete": false,
                    "modified_time": null,
                    "plural_label": "Actions Performed",
                    "presence_sub_menu": false,
                    "actual_plural_label": "Actions Performed",
                    "lookupable": false,
                    "id": "738692000000081005",
                    "isBlueprintSupported": false,
                    "visibility": 1,
                    "convertable": false,
                    "sub_menu_available": false,
                    "editable": false,
                    "actual_singular_label": "Actions Performed",
                    "profiles":
                    [
                        {
                            "name": "Administrator",
                            "id": "738692000000026972"
                        },
                        {
                            "name": "Standard",
                            "id": "738692000000026974"
                        }
                    ],
                    "show_as_tab": false,
                    "web_link": null,
                    "sequence_number": 41,
                    "singular_label": "Actions Performed",
                    "viewable": true,
                    "api_supported": true,
                    "api_name": "Actions_Performed",
                    "quick_create": false,
                    "modified_by": null,
                    "generated_type": "default",
                    "feeds_required": false,
                    "public_fields_configured": false,
                    "arguments":
                    [],
                    "module_name": "Actions Performed",
                    "profile_count": 2,
                    "business_card_field_limit": 5,
                    "parent_module":
                    {},
                    "status": "system_hidden"
                },
                {
                    "has_more_profiles": false,
                    "access_type": "org_based",
                    "private_profile": null,
                    "global_search_supported": false,
                    "deletable": false,
                    "description": null,
                    "creatable": false,
                    "recycle_bin_on_delete": false,
                    "modified_time": null,
                    "plural_label": "ShiftHours",
                    "presence_sub_menu": false,
                    "actual_plural_label": "ShiftHours",
                    "lookupable": false,
                    "id": "738692000000225011",
                    "isBlueprintSupported": false,
                    "visibility": 14334,
                    "convertable": false,
                    "sub_menu_available": false,
                    "editable": false,
                    "actual_singular_label": "ShiftHour",
                    "profiles":
                    [
                        {
                            "name": "Administrator",
                            "id": "738692000000026972"
                        },
                        {
                            "name": "Standard",
                            "id": "738692000000026974"
                        }
                    ],
                    "show_as_tab": false,
                    "web_link": null,
                    "sequence_number": 58,
                    "singular_label": "ShiftHour",
                    "viewable": false,
                    "api_supported": false,
                    "api_name": "ShiftHours",
                    "quick_create": false,
                    "modified_by": null,
                    "generated_type": "default",
                    "feeds_required": false,
                    "public_fields_configured": false,
                    "arguments":
                    [],
                    "module_name": "ShiftHours",
                    "profile_count": 2,
                    "business_card_field_limit": 5,
                    "parent_module":
                    {},
                    "status": "visible"
                },
                {
                    "has_more_profiles": false,
                    "access_type": "org_based",
                    "private_profile": null,
                    "global_search_supported": false,
                    "deletable": false,
                    "description": null,
                    "creatable": false,
                    "recycle_bin_on_delete": false,
                    "modified_time": null,
                    "plural_label": "Forecast Targets",
                    "presence_sub_menu": false,
                    "actual_plural_label": "Forecast Targets",
                    "lookupable": false,
                    "id": "738692000000250017",
                    "isBlueprintSupported": false,
                    "visibility": 736,
                    "convertable": false,
                    "sub_menu_available": false,
                    "editable": false,
                    "actual_singular_label": "Forecast Target",
                    "profiles":
                    [
                        {
                            "name": "Administrator",
                            "id": "738692000000026972"
                        },
                        {
                            "name": "Standard",
                            "id": "738692000000026974"
                        }
                    ],
                    "show_as_tab": false,
                    "web_link": null,
                    "sequence_number": 59,
                    "singular_label": "Forecast Target",
                    "viewable": false,
                    "api_supported": false,
                    "api_name": "Forecast_Quotas",
                    "quick_create": false,
                    "modified_by": null,
                    "generated_type": "default",
                    "feeds_required": false,
                    "public_fields_configured": false,
                    "arguments":
                    [],
                    "module_name": "Forecast Quotas",
                    "profile_count": 2,
                    "business_card_field_limit": 5,
                    "parent_module":
                    {},
                    "status": "system_hidden"
                },
                {
                    "has_more_profiles": false,
                    "access_type": "org_based",
                    "private_profile": null,
                    "global_search_supported": false,
                    "deletable": false,
                    "description": null,
                    "creatable": false,
                    "recycle_bin_on_delete": false,
                    "modified_time": null,
                    "plural_label": "Forecast Items",
                    "presence_sub_menu": false,
                    "actual_plural_label": "Forecast Items",
                    "lookupable": false,
                    "id": "738692000000250019",
                    "isBlueprintSupported": false,
                    "visibility": 736,
                    "convertable": false,
                    "sub_menu_available": false,
                    "editable": false,
                    "actual_singular_label": "Forecast Item",
                    "profiles":
                    [
                        {
                            "name": "Administrator",
                            "id": "738692000000026972"
                        },
                        {
                            "name": "Standard",
                            "id": "738692000000026974"
                        }
                    ],
                    "show_as_tab": false,
                    "web_link": null,
                    "sequence_number": 59,
                    "singular_label": "Forecast Item",
                    "viewable": false,
                    "api_supported": false,
                    "api_name": "Forecast_Items",
                    "quick_create": false,
                    "modified_by": null,
                    "generated_type": "default",
                    "feeds_required": false,
                    "public_fields_configured": false,
                    "arguments":
                    [],
                    "module_name": "Forecast Items",
                    "profile_count": 2,
                    "business_card_field_limit": 5,
                    "parent_module":
                    {},
                    "status": "system_hidden"
                },
                {
                    "has_more_profiles": false,
                    "access_type": "org_based",
                    "private_profile": null,
                    "global_search_supported": false,
                    "deletable": false,
                    "description": null,
                    "creatable": false,
                    "recycle_bin_on_delete": false,
                    "modified_time": null,
                    "plural_label": "Forecast Groups",
                    "presence_sub_menu": false,
                    "actual_plural_label": "Forecast Groups",
                    "lookupable": false,
                    "id": "738692000000250027",
                    "isBlueprintSupported": false,
                    "visibility": 2044,
                    "convertable": false,
                    "sub_menu_available": false,
                    "editable": false,
                    "actual_singular_label": "Forecast Group",
                    "profiles":
                    [
                        {
                            "name": "Administrator",
                            "id": "738692000000026972"
                        },
                        {
                            "name": "Standard",
                            "id": "738692000000026974"
                        }
                    ],
                    "show_as_tab": false,
                    "web_link": null,
                    "sequence_number": 59,
                    "singular_label": "Forecast Group",
                    "viewable": false,
                    "api_supported": false,
                    "api_name": "Forecast_Groups",
                    "quick_create": false,
                    "modified_by": null,
                    "generated_type": "default",
                    "feeds_required": false,
                    "public_fields_configured": false,
                    "arguments":
                    [],
                    "module_name": "Forecast Groups",
                    "profile_count": 2,
                    "business_card_field_limit": 5,
                    "parent_module":
                    {},
                    "status": "system_hidden"
                },
                {
                    "has_more_profiles": false,
                    "access_type": "org_based",
                    "private_profile": null,
                    "global_search_supported": false,
                    "deletable": false,
                    "description": null,
                    "creatable": false,
                    "recycle_bin_on_delete": false,
                    "modified_time": null,
                    "plural_label": "Locking Information",
                    "presence_sub_menu": false,
                    "actual_plural_label": "Locking Information",
                    "lookupable": false,
                    "id": "738692000000313001",
                    "isBlueprintSupported": false,
                    "visibility": 2,
                    "convertable": false,
                    "sub_menu_available": false,
                    "editable": false,
                    "actual_singular_label": "Locking Information",
                    "profiles":
                    [
                        {
                            "name": "Administrator",
                            "id": "738692000000026972"
                        },
                        {
                            "name": "Standard",
                            "id": "738692000000026974"
                        }
                    ],
                    "show_as_tab": false,
                    "web_link": null,
                    "sequence_number": 72,
                    "singular_label": "Locking Information",
                    "viewable": false,
                    "api_supported": true,
                    "api_name": "Locking_Information__s",
                    "quick_create": false,
                    "modified_by": null,
                    "generated_type": "default",
                    "feeds_required": false,
                    "public_fields_configured": false,
                    "arguments":
                    [],
                    "module_name": "LockingInformation",
                    "profile_count": 2,
                    "business_card_field_limit": 5,
                    "parent_module":
                    {},
                    "status": "visible"
                },
                {
                    "has_more_profiles": false,
                    "access_type": "org_based",
                    "private_profile": null,
                    "global_search_supported": false,
                    "deletable": false,
                    "description": null,
                    "creatable": false,
                    "recycle_bin_on_delete": false,
                    "modified_time": "2024-09-27T14:46:48+02:00",
                    "plural_label": "Projects",
                    "presence_sub_menu": false,
                    "actual_plural_label": "Projects",
                    "lookupable": false,
                    "id": "738692000000432025",
                    "isBlueprintSupported": false,
                    "visibility": 1,
                    "convertable": false,
                    "sub_menu_available": false,
                    "editable": false,
                    "actual_singular_label": "Projects",
                    "profiles":
                    [],
                    "show_as_tab": true,
                    "web_link": null,
                    "sequence_number": 111,
                    "singular_label": "Projects",
                    "viewable": false,
                    "api_supported": false,
                    "api_name": "Projects",
                    "quick_create": false,
                    "modified_by":
                    {
                        "name": "Daniel García",
                        "id": "738692000000414001"
                    },
                    "generated_type": "default",
                    "feeds_required": false,
                    "public_fields_configured": false,
                    "arguments":
                    [],
                    "module_name": "Projects",
                    "profile_count": 0,
                    "business_card_field_limit": 5,
                    "parent_module":
                    {},
                    "status": "user_hidden"
                },
                {
                    "has_more_profiles": false,
                    "access_type": "org_based",
                    "private_profile": null,
                    "global_search_supported": true,
                    "deletable": true,
                    "description": null,
                    "creatable": true,
                    "recycle_bin_on_delete": true,
                    "modified_time": "2024-10-08T14:57:50+02:00",
                    "plural_label": "Estudiantes",
                    "presence_sub_menu": false,
                    "actual_plural_label": "Estudiantes",
                    "lookupable": false,
                    "id": "738692000000557017",
                    "isBlueprintSupported": false,
                    "visibility": 1,
                    "convertable": false,
                    "sub_menu_available": true,
                    "editable": true,
                    "actual_singular_label": "Estudiante",
                    "profiles":
                    [
                        {
                            "name": "Administrator",
                            "id": "738692000000026972"
                        }
                    ],
                    "show_as_tab": true,
                    "web_link": null,
                    "sequence_number": 112,
                    "singular_label": "Estudiante",
                    "viewable": true,
                    "api_supported": true,
                    "api_name": "Estudiantes",
                    "quick_create": false,
                    "modified_by":
                    {
                        "name": "Daniel García",
                        "id": "738692000000414001"
                    },
                    "generated_type": "custom",
                    "feeds_required": false,
                    "public_fields_configured": false,
                    "arguments":
                    [],
                    "module_name": "CustomModule2",
                    "profile_count": 1,
                    "business_card_field_limit": 5,
                    "parent_module":
                    {},
                    "status": "user_hidden"
                }
            ]
        }
        """
        response_object = response.json()

        for module in response_object["modules"]:
            yield BaseModule(module, module["module_name"], module["id"])

    def __get_module_by_name(self, module_name: str) -> dict:
        url = f"{self.auth.api_domain}/crm/v7/settings/modules/{module_name}"

        response = requests.get(url, headers=self.auth.http_headers)

        if response.status_code != 200:
            raise ZohoCRMException(f"Error getting module {module_name}")

        response_object = response.json()

        try:
            return response_object["modules"][0]
        except (IndexError, KeyError):
            raise ZohoCRMException(f"BaseModule {module_name} not found")

    def get_module(self, module_name: str) -> BaseModule:
        return BaseModule.from_api(
            self.auth,
            self.__get_module_by_name(module_name)
        )

    def get_leads_module(self) -> ZohoLeads:
        m = self.__get_module_by_name(ModulesNames.LEADS)
        return ZohoLeads.from_api(self.auth, m)

    def get_contacts_module(self) -> ZohoContacts:
        m = self.__get_module_by_name(ModulesNames.CONTACTS)
        return ZohoContacts.from_api(self.auth, m)

    def get_purchase_orders_module(self) -> ZohoPurchaseOrders:
        m = self.__get_module_by_name(ModulesNames.PURCHASE_ORDERS)
        return ZohoPurchaseOrders.from_api(self.auth, m)

    def get_products_module(self) -> ZohoProducts:
        m = self.__get_module_by_name(ModulesNames.PRODUCTS)
        return ZohoProducts.from_api(self.auth, m)

    def get_course_progress_module(self) -> ZohoCourseProgress:
        m = self.__get_module_by_name(ModulesNames.COURSE_PROGRESS)
        return ZohoCourseProgress.from_api(self.auth, m)


__all__ = ("ZohoCRM",)
