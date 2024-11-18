import requests

# https://www.zoho.com/crm/developer/docs/api/v7/modules-api.html
def main():

    headers = {
        'Authorization': 'Zoho-oauthtoken 1000.2c501e600446ebf56c4a4093585f2542.3c55c33755c0c28d9ed5f5d3c5e37c1b',
        'X-ZOHO-SDK': 'Darwin/23.6.0/python-7.0/3.11.9:3.0.0'
    }
    # print("Modules:")
    #
    url = 'https://www.zohoapis.eu/crm/v7/settings/modules'
    response = requests.get(url, headers=headers)
    # print(data.json())
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
    print(response.text)

    url = 'https://www.zohoapis.eu/crm/v7/settings/modules/Purchase_Orders'
    response = requests.get(url, headers=headers)
    # print(data.json())
    """
    data in JSON:
    
    {
    "modules":
        [
            {
                "private_profile": null,
                "global_search_supported": true,
                "activity_badge": "Not_Supported",
                "$field_states":
                [
                    "convert_scheduler"
                ],
                "recycle_bin_on_delete": true,
                "plural_label": "Purchase Orders",
                "presence_sub_menu": true,
                "chart_view": false,
                "id": "738692000000000109",
                "per_page": 50,
                "$properties":
                [
                    "$line_tax",
                    "$approval_state",
                    "$wizard_connection_path",
                    "$cpq_executions",
                    "$currency_symbol",
                    "$review",
                    "$review_process",
                    "$approval",
                    "$in_merge",
                    "$process_flow",
                    "$orchestration",
                    "$pathfinder",
                    "$zia_visions",
                    "$editable",
                    "$field_states",
                    "$locked_for_me",
                    "$has_more",
                    "$sharing_permission"
                ],
                "visibility": 1,
                "sub_menu_available": true,
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
                "$on_demand_properties":
                [
                    "$blocked_reason"
                ],
                "kanban_view_supported": true,
                "web_link": null,
                "lookup_field_properties":
                {
                    "fields":
                    [
                        {
                            "sequence_number": 1,
                            "api_name": "Subject",
                            "id": "738692000000002071"
                        },
                        {
                            "sequence_number": 2,
                            "api_name": "Grand_Total",
                            "id": "738692000000002107"
                        },
                        {
                            "sequence_number": 3,
                            "api_name": "Contact_Name",
                            "id": "738692000000002075"
                        },
                        {
                            "sequence_number": 4,
                            "api_name": "PO_Date",
                            "id": "738692000000002077"
                        },
                        {
                            "sequence_number": 5,
                            "api_name": "ID_EzyCourse",
                            "id": "738692000000759139"
                        }
                    ]
                },
                "viewable": true,
                "api_name": "Purchase_Orders",
                "public_fields_configured": false,
                "module_name": "PurchaseOrders",
                "chart_view_supported": true,
                "custom_view":
                {
                    "display_value": "All Purchase Orders",
                    "created_time": null,
                    "access_type": "public",
                    "criteria": null,
                    "system_name": "ALLVIEWS",
                    "sort_by": null,
                    "created_by": null,
                    "shared_to": null,
                    "default": true,
                    "modified_time": "2024-11-06T12:59:29+01:00",
                    "name": "All PurchaseOrders",
                    "system_defined": true,
                    "modified_by":
                    {
                        "name": "Daniel García",
                        "id": "738692000000414001"
                    },
                    "id": "738692000000031151",
                    "fields":
                    [
                        {
                            "api_name": "Subject",
                            "_pin": false,
                            "id": "738692000000002071"
                        },
                        {
                            "api_name": "Grand_Total",
                            "_pin": false,
                            "id": "738692000000002107"
                        },
                        {
                            "api_name": "Contact_Name",
                            "_pin": false,
                            "id": "738692000000002075"
                        },
                        {
                            "api_name": "PO_Date",
                            "_pin": false,
                            "id": "738692000000002077"
                        },
                        {
                            "api_name": "ID_EzyCourse",
                            "_pin": false,
                            "id": "738692000000759139"
                        }
                    ],
                    "category": "public_views",
                    "last_accessed_time": "2024-11-14T11:16:00+01:00",
                    "locked": false,
                    "sort_order": null,
                    "favorite": null
                },
                "parent_module":
                {},
                "status": "visible",
                "has_more_profiles": false,
                "access_type": "org_based",
                "kanban_view": false,
                "deletable": true,
                "description": null,
                "creatable": true,
                "filter_status": true,
                "modified_time": "2024-10-09T16:26:27+02:00",
                "actual_plural_label": "Purchase Orders",
                "lookupable": true,
                "isBlueprintSupported": true,
                "related_list_properties":
                {
                    "sort_by": null,
                    "fields":
                    [
                        "Subject",
                        "Status",
                        "Due_Date",
                        "Excise_Duty",
                        "Sales_Commission"
                    ],
                    "sort_order": null
                },
                "convertable": false,
                "editable": true,
                "actual_singular_label": "Purchase Order",
                "display_field": "Subject",
                "search_layout_fields":
                [
                    "Subject",
                    "Contact_Name",
                    "Status",
                    "Owner",
                    "Grand_Total"
                ],
                "show_as_tab": true,
                "sequence_number": 5,
                "singular_label": "Purchase Order",
                "api_supported": true,
                "quick_create": true,
                "modified_by":
                {
                    "name": "Daniel García",
                    "id": "738692000000414001"
                },
                "generated_type": "default",
                "feeds_required": false,
                "arguments":
                [],
                "profile_count": 2,
                "business_card_field_limit": 5
            }
        ]
    }
    """
    print(response.text)

    # print("BaseModule properties:")
    # url = "https://www.zohoapis.com/crm/v7/settings/fields?module=Purchase_Orders"
    # data = requests.get(url, headers=headers)
    # print(data.json())
    # print(data.text)

    # print("List Purchase Orders:")
    url = 'https://www.zohoapis.eu/crm/v7/Purchase_Orders'
    params = {
        'page': '1',
        'per_page': '50',
        'fields': 'Subject,ID_EzyCourse,id,PO_Date,PO_Status,Purchased_Items,Grand_Total,Contact_Name',
        'include_child': 'true'
    }

    response = requests.get(url, headers=headers, params=params)
    """
    data in JSON:
    
    {
        "data":
        [
            {
                "Grand_Total": 49,
                "PO_Date": "2024-11-06",
                "ID_EzyCourse": 10978,
                "id": "738692000001258147",
                "Subject": "301 - Ocultación y ejecución de código Python",
                "Contact_Name": null
            },
            {
                "Grand_Total": 49,
                "PO_Date": "2024-11-06",
                "ID_EzyCourse": 10978,
                "id": "738692000001258131",
                "Subject": "301 - Ocultación y ejecución de código Python",
                "Contact_Name":
                {
                    "name": "Jesus Garcia None",
                    "id": "738692000000680146"
                }
            },
            {
                "Grand_Total": 49,
                "PO_Date": "2024-11-06",
                "ID_EzyCourse": 10978,
                "id": "738692000001258119",
                "Subject": "301 - Ocultación y ejecución de código Python",
                "Contact_Name":
                {
                    "name": "Braiant Giraldo None",
                    "id": "738692000000679715"
                }
            },
            {
                "Grand_Total": 49,
                "PO_Date": "2024-11-06",
                "ID_EzyCourse": 10978,
                "id": "738692000001258107",
                "Subject": "301 - Ocultación y ejecución de código Python",
                "Contact_Name":
                {
                    "name": "Jorge Calleja None",
                    "id": "738692000000679709"
                }
            },
            {
                "Grand_Total": 49,
                "PO_Date": "2024-11-06",
                "ID_EzyCourse": 10978,
                "id": "738692000001258095",
                "Subject": "301 - Ocultación y ejecución de código Python",
                "Contact_Name":
                {
                    "name": "Cristian Rebollo None",
                    "id": "738692000000679688"
                }
            },
            {
                "Grand_Total": 49,
                "PO_Date": "2024-11-06",
                "ID_EzyCourse": 10978,
                "id": "738692000001258083",
                "Subject": "301 - Ocultación y ejecución de código Python",
                "Contact_Name":
                {
                    "name": "Fernando Rios None",
                    "id": "738692000000679659"
                }
            },
            {
                "Grand_Total": 49,
                "PO_Date": "2024-11-06",
                "ID_EzyCourse": 10978,
                "id": "738692000001258071",
                "Subject": "301 - Ocultación y ejecución de código Python",
                "Contact_Name":
                {
                    "name": "César Fernandez Gonzalez None",
                    "id": "738692000000679167"
                }
            },
            {
                "Grand_Total": 49,
                "PO_Date": "2024-11-06",
                "ID_EzyCourse": 10978,
                "id": "738692000001258059",
                "Subject": "301 - Ocultación y ejecución de código Python",
                "Contact_Name":
                {
                    "name": "Julian Fonticoba None",
                    "id": "738692000000680202"
                }
            },
            {
                "Grand_Total": 49,
                "PO_Date": "2024-11-06",
                "ID_EzyCourse": 10978,
                "id": "738692000001258047",
                "Subject": "301 - Ocultación y ejecución de código Python",
                "Contact_Name":
                {
                    "name": "Jonathan Planells None",
                    "id": "738692000000679552"
                }
            },
            {
                "Grand_Total": 49,
                "PO_Date": "2024-11-06",
                "ID_EzyCourse": 10978,
                "id": "738692000001258035",
                "Subject": "301 - Ocultación y ejecución de código Python",
                "Contact_Name":
                {
                    "name": "Alberto Martin None",
                    "id": "738692000000680162"
                }
            },
            {
                "Grand_Total": 49,
                "PO_Date": "2024-11-06",
                "ID_EzyCourse": 10978,
                "id": "738692000001258023",
                "Subject": "301 - Ocultación y ejecución de código Python",
                "Contact_Name":
                {
                    "name": "andres pozo None",
                    "id": "738692000000679550"
                }
            },
            {
                "Grand_Total": 49,
                "PO_Date": "2024-11-06",
                "ID_EzyCourse": 10978,
                "id": "738692000001257207",
                "Subject": "301 - Ocultación y ejecución de código Python",
                "Contact_Name":
                {
                    "name": "M D None",
                    "id": "738692000000680123"
                }
            },
            {
                "Grand_Total": 49,
                "PO_Date": "2024-11-06",
                "ID_EzyCourse": 10978,
                "id": "738692000001257195",
                "Subject": "301 - Ocultación y ejecución de código Python",
                "Contact_Name":
                {
                    "name": "Jose Lopez None",
                    "id": "738692000000680055"
                }
            },
            {
                "Grand_Total": 49,
                "PO_Date": "2024-11-06",
                "ID_EzyCourse": 10978,
                "id": "738692000001257183",
                "Subject": "301 - Ocultación y ejecución de código Python",
                "Contact_Name":
                {
                    "name": "Felipe Caudillo None",
                    "id": "738692000000679724"
                }
            },
            {
                "Grand_Total": 49,
                "PO_Date": "2024-11-06",
                "ID_EzyCourse": 10978,
                "id": "738692000001257171",
                "Subject": "301 - Ocultación y ejecución de código Python",
                "Contact_Name":
                {
                    "name": "Hector Garcia None",
                    "id": "738692000000679215"
                }
            },
            {
                "Grand_Total": 49,
                "PO_Date": "2024-11-06",
                "ID_EzyCourse": 10978,
                "id": "738692000001257159",
                "Subject": "301 - Ocultación y ejecución de código Python",
                "Contact_Name":
                {
                    "name": "Hugo Lozano Hermida None",
                    "id": "738692000000679598"
                }
            },
            {
                "Grand_Total": 49,
                "PO_Date": "2024-11-06",
                "ID_EzyCourse": 10978,
                "id": "738692000001257147",
                "Subject": "301 - Ocultación y ejecución de código Python",
                "Contact_Name":
                {
                    "name": "Alex Hernandez None",
                    "id": "738692000000679573"
                }
            },
            {
                "Grand_Total": 49,
                "PO_Date": "2024-11-06",
                "ID_EzyCourse": 10978,
                "id": "738692000001257135",
                "Subject": "301 - Ocultación y ejecución de código Python",
                "Contact_Name":
                {
                    "name": "Noko None",
                    "id": "738692000000679566"
                }
            },
            {
                "Grand_Total": 49,
                "PO_Date": "2024-11-06",
                "ID_EzyCourse": 10978,
                "id": "738692000001257123",
                "Subject": "301 - Ocultación y ejecución de código Python",
                "Contact_Name":
                {
                    "name": "Pablo De la Morena None",
                    "id": "738692000000679563"
                }
            },
            {
                "Grand_Total": 49,
                "PO_Date": "2024-11-06",
                "ID_EzyCourse": 10978,
                "id": "738692000001257111",
                "Subject": "301 - Ocultación y ejecución de código Python",
                "Contact_Name":
                {
                    "name": "Mario Lima None",
                    "id": "738692000000680264"
                }
            },
            {
                "Grand_Total": 49,
                "PO_Date": "2024-11-06",
                "ID_EzyCourse": 10978,
                "id": "738692000001257099",
                "Subject": "301 - Ocultación y ejecución de código Python",
                "Contact_Name":
                {
                    "name": "Snifer Sniferl4bs None",
                    "id": "738692000000680257"
                }
            },
            {
                "Grand_Total": 49,
                "PO_Date": "2024-11-06",
                "ID_EzyCourse": 10978,
                "id": "738692000001257087",
                "Subject": "301 - Ocultación y ejecución de código Python",
                "Contact_Name":
                {
                    "name": "Raúl Leal",
                    "id": "738692000000680238"
                }
            },
            {
                "Grand_Total": 49,
                "PO_Date": "2024-11-06",
                "ID_EzyCourse": 10978,
                "id": "738692000001257075",
                "Subject": "301 - Ocultación y ejecución de código Python",
                "Contact_Name":
                {
                    "name": "Fran Romero None",
                    "id": "738692000000680180"
                }
            },
            {
                "Grand_Total": 49,
                "PO_Date": "2024-11-06",
                "ID_EzyCourse": 10978,
                "id": "738692000001257063",
                "Subject": "301 - Ocultación y ejecución de código Python",
                "Contact_Name":
                {
                    "name": "Raúl Sesb None",
                    "id": "738692000000680173"
                }
            },
            {
                "Grand_Total": 49,
                "PO_Date": "2024-11-06",
                "ID_EzyCourse": 10978,
                "id": "738692000001257051",
                "Subject": "301 - Ocultación y ejecución de código Python",
                "Contact_Name":
                {
                    "name": "Juan De la Fuente None",
                    "id": "738692000000679078"
                }
            },
            {
                "Grand_Total": 49,
                "PO_Date": "2024-11-06",
                "ID_EzyCourse": 10978,
                "id": "738692000001257039",
                "Subject": "301 - Ocultación y ejecución de código Python",
                "Contact_Name":
                {
                    "name": "Gerar Ruiz None",
                    "id": "738692000000679242"
                }
            },
            {
                "Grand_Total": 49,
                "PO_Date": "2024-11-06",
                "ID_EzyCourse": 12602,
                "id": "738692000001257027",
                "Subject": "101 - Introducción seguridad APIs REST",
                "Contact_Name":
                {
                    "name": "Diego Aznar Motiones",
                    "id": "738692000000680281"
                }
            },
            {
                "Grand_Total": 49,
                "PO_Date": "2024-11-06",
                "ID_EzyCourse": 10978,
                "id": "738692000001256169",
                "Subject": "301 - Ocultación y ejecución de código Python",
                "Contact_Name":
                {
                    "name": "Juan Diego Sierra Fernández None",
                    "id": "738692000000680145"
                }
            },
            {
                "Grand_Total": 49,
                "PO_Date": "2024-11-06",
                "ID_EzyCourse": 10978,
                "id": "738692000001256157",
                "Subject": "301 - Ocultación y ejecución de código Python",
                "Contact_Name":
                {
                    "name": "Byron Gonzalez None",
                    "id": "738692000000680101"
                }
            },
            {
                "Grand_Total": 49,
                "PO_Date": "2024-11-06",
                "ID_EzyCourse": 10978,
                "id": "738692000001256134",
                "Subject": "301 - Ocultación y ejecución de código Python",
                "Contact_Name":
                {
                    "name": "Mauricio Vargas None",
                    "id": "738692000000680090"
                }
            },
            {
                "Grand_Total": 49,
                "PO_Date": "2024-11-06",
                "ID_EzyCourse": 10978,
                "id": "738692000001256133",
                "Subject": "301 - Ocultación y ejecución de código Python",
                "Contact_Name":
                {
                    "name": "Alan Arlenko None",
                    "id": "738692000000680089"
                }
            },
            {
                "Grand_Total": 49,
                "PO_Date": "2024-11-06",
                "ID_EzyCourse": 10978,
                "id": "738692000001256121",
                "Subject": "301 - Ocultación y ejecución de código Python",
                "Contact_Name":
                {
                    "name": "Tom Gilabert None",
                    "id": "738692000000679785"
                }
            },
            {
                "Grand_Total": 49,
                "PO_Date": "2024-11-06",
                "ID_EzyCourse": 10978,
                "id": "738692000001256109",
                "Subject": "301 - Ocultación y ejecución de código Python",
                "Contact_Name":
                {
                    "name": "Jordi Vidal None",
                    "id": "738692000000679774"
                }
            },
            {
                "Grand_Total": 49,
                "PO_Date": "2024-11-06",
                "ID_EzyCourse": 10978,
                "id": "738692000001256097",
                "Subject": "301 - Ocultación y ejecución de código Python",
                "Contact_Name":
                {
                    "name": "Raúl Martínez Ortiz None",
                    "id": "738692000000679769"
                }
            },
            {
                "Grand_Total": 49,
                "PO_Date": "2024-11-06",
                "ID_EzyCourse": 10978,
                "id": "738692000001256085",
                "Subject": "301 - Ocultación y ejecución de código Python",
                "Contact_Name":
                {
                    "name": "Juan Sánchez None",
                    "id": "738692000000679743"
                }
            },
            {
                "Grand_Total": 49,
                "PO_Date": "2024-11-06",
                "ID_EzyCourse": 10978,
                "id": "738692000001256073",
                "Subject": "301 - Ocultación y ejecución de código Python",
                "Contact_Name":
                {
                    "name": "Jonatan Escobar None",
                    "id": "738692000000679662"
                }
            },
            {
                "Grand_Total": 49,
                "PO_Date": "2024-11-06",
                "ID_EzyCourse": 10978,
                "id": "738692000001256061",
                "Subject": "301 - Ocultación y ejecución de código Python",
                "Contact_Name":
                {
                    "name": "Indira Franchi None",
                    "id": "738692000000679615"
                }
            },
            {
                "Grand_Total": 49,
                "PO_Date": "2024-11-06",
                "ID_EzyCourse": 10978,
                "id": "738692000001256049",
                "Subject": "301 - Ocultación y ejecución de código Python",
                "Contact_Name":
                {
                    "name": "Alex Alvarez None",
                    "id": "738692000000679603"
                }
            },
            {
                "Grand_Total": 49,
                "PO_Date": "2024-11-06",
                "ID_EzyCourse": 10978,
                "id": "738692000001256037",
                "Subject": "301 - Ocultación y ejecución de código Python",
                "Contact_Name":
                {
                    "name": "M M None",
                    "id": "738692000000679568"
                }
            },
            {
                "Grand_Total": 49,
                "PO_Date": "2024-11-06",
                "ID_EzyCourse": 10978,
                "id": "738692000001256025",
                "Subject": "301 - Ocultación y ejecución de código Python",
                "Contact_Name":
                {
                    "name": "Ivan Gomez None",
                    "id": "738692000000679040"
                }
            },
            {
                "Grand_Total": 49,
                "PO_Date": "2024-11-06",
                "ID_EzyCourse": 10978,
                "id": "738692000001256013",
                "Subject": "301 - Ocultación y ejecución de código Python",
                "Contact_Name":
                {
                    "name": "Eduardo Sayus None",
                    "id": "738692000000680192"
                }
            },
            {
                "Grand_Total": 49,
                "PO_Date": "2024-11-06",
                "ID_EzyCourse": 10978,
                "id": "738692000001255143",
                "Subject": "301 - Ocultación y ejecución de código Python",
                "Contact_Name":
                {
                    "name": "Nicolás Guillén None",
                    "id": "738692000000680126"
                }
            },
            {
                "Grand_Total": 49,
                "PO_Date": "2024-11-06",
                "ID_EzyCourse": 10978,
                "id": "738692000001255131",
                "Subject": "301 - Ocultación y ejecución de código Python",
                "Contact_Name":
                {
                    "name": "Eric Avila None",
                    "id": "738692000000680085"
                }
            },
            {
                "Grand_Total": 49,
                "PO_Date": "2024-11-06",
                "ID_EzyCourse": 10978,
                "id": "738692000001255119",
                "Subject": "301 - Ocultación y ejecución de código Python",
                "Contact_Name":
                {
                    "name": "Alberto Villegas None",
                    "id": "738692000000680102"
                }
            },
            {
                "Grand_Total": 49,
                "PO_Date": "2024-11-06",
                "ID_EzyCourse": 10978,
                "id": "738692000001255107",
                "Subject": "301 - Ocultación y ejecución de código Python",
                "Contact_Name":
                {
                    "name": "Elena Vegas None",
                    "id": "738692000000679706"
                }
            },
            {
                "Grand_Total": 49,
                "PO_Date": "2024-11-06",
                "ID_EzyCourse": 10978,
                "id": "738692000001255095",
                "Subject": "301 - Ocultación y ejecución de código Python",
                "Contact_Name":
                {
                    "name": "jox 115 None",
                    "id": "738692000000679670"
                }
            },
            {
                "Grand_Total": 49,
                "PO_Date": "2024-11-06",
                "ID_EzyCourse": 10978,
                "id": "738692000001255083",
                "Subject": "301 - Ocultación y ejecución de código Python",
                "Contact_Name":
                {
                    "name": "Alfred Finel None",
                    "id": "738692000000679665"
                }
            },
            {
                "Grand_Total": 49,
                "PO_Date": "2024-11-06",
                "ID_EzyCourse": 10978,
                "id": "738692000001255071",
                "Subject": "301 - Ocultación y ejecución de código Python",
                "Contact_Name":
                {
                    "name": "Tomeu Roig None",
                    "id": "738692000000679620"
                }
            },
            {
                "Grand_Total": 49,
                "PO_Date": "2024-11-06",
                "ID_EzyCourse": 10978,
                "id": "738692000001255059",
                "Subject": "301 - Ocultación y ejecución de código Python",
                "Contact_Name":
                {
                    "name": "Ana Gazo None",
                    "id": "738692000000679575"
                }
            },
            {
                "Grand_Total": 49,
                "PO_Date": "2024-11-06",
                "ID_EzyCourse": 10978,
                "id": "738692000001255047",
                "Subject": "301 - Ocultación y ejecución de código Python",
                "Contact_Name":
                {
                    "name": "David Soto Dalmau None",
                    "id": "738692000000679281"
                }
            }
        ],
        "info":
        {
            "per_page": 50,
            "next_page_token": "2332a2b8e65a59ca54fc853154470404adbbf29050553afde4533612bd8c80243120b23c82e0d28143888c5d2e9d553fce6bd7050668fa87bf9dc7a78a38e38e3641cb340e172e41b155f5e5e37675545028a30311771f2b95ed513711dfbbe874d041b4e2afad025c0fb99fe52b024c8271de76fecb138a0367fa91a6f90c02",
            "count": 50,
            "sort_by": "id",
            "page": 1,
            "previous_page_token": null,
            "page_token_expiry": "2024-11-15T12:38:06+01:00",
            "sort_order": "desc",
            "more_records": true
        }
    }
        """
    print(response.text)

    print("Purchase Order details:")
    url = 'https://www.zohoapis.eu/crm/v7/Purchase_Orders/738692000001258147'
    response = requests.get(url, headers=headers)
    """
    Response in JSON:
    {
    "data":
        [
            {
                "Owner":
                {
                    "name": "Daniel García",
                    "id": "738692000000414001",
                    "email": "hello@alicebob.io"
                },
                "$currency_symbol": "€",
                "$field_states": null,
                "Tax": 0,
                "$sharing_permission": "full_access",
                "PO_Date": "2024-11-06",
                "$process_flow": false,
                "Billing_Country": null,
                "$locked_for_me": false,
                "id": "738692000001258147",
                "Carrier": "No Aplica",
                "Status": "Entregado",
                "Grand_Total": 49,
                "$approval":
                {
                    "delegate": false,
                    "takeover": false,
                    "approve": false,
                    "reject": false,
                    "resubmit": false
                },
                "Billing_Street": null,
                "Adjustment": 0,
                "$wizard_connection_path": null,
                "$editable": true,
                "Billing_Code": null,
                "Excise_Duty": null,
                "Shipping_City": null,
                "Shipping_Country": null,
                "Shipping_Code": null,
                "Billing_City": null,
                "ID_EzyCourse": 10978,
                "Shipping_Street": null,
                "Description": null,
                "Discount": 0,
                "Shipping_State": null,
                "$review_process":
                {
                    "approve": false,
                    "reject": false,
                    "resubmit": false
                },
                "$canvas_id": null,
                "Modified_By":
                {
                    "name": "Daniel García",
                    "id": "738692000000414001",
                    "email": "hello@alicebob.io"
                },
                "$review": null,
                "Purchase_Items":
                [
                    {
                        "Modified_Time": "2024-11-06T16:26:58+01:00",
                        "Description": null,
                        "Discount": 0,
                        "$field_states": null,
                        "Created_Time": "2024-11-06T16:26:58+01:00",
                        "Parent_Id":
                        {
                            "name": "301 - Ocultación y ejecución de código Python",
                            "id": "738692000001258147"
                        },
                        "Product_Name":
                        {
                            "Product_Code": null,
                            "Qty_Ordered": 0,
                            "Layout":
                            {
                                "id": "738692000000032007"
                            },
                            "name": "301 - Ocultación y ejecución de código Python",
                            "Qty_in_Stock": 433,
                            "Tax":
                            [
                                {
                                    "id": "738692000000414582",
                                    "value": "IVA - 0.0 %"
                                }
                            ],
                            "id": "738692000000695355",
                            "Taxable": true,
                            "Unit_Price": 49,
                            "Reorder_Level": 0
                        },
                        "Quantity": 1,
                        "Tax": 0,
                        "Net_Total": 49,
                        "Total": 49,
                        "Line_Tax":
                        [
                            {
                                "percentage": 0,
                                "name": "IVA",
                                "id": "738692000000414582",
                                "value": 0
                            }
                        ],
                        "List_Price": 49,
                        "id": "738692000001258149",
                        "$zia_visions": null,
                        "Total_After_Discount": 49
                    }
                ],
                "$zia_visions": null,
                "Sales_Commission": null,
                "Modified_Time": "2024-11-06T16:26:58+01:00",
                "Due_Date": null,
                "Terms_and_Conditions": null,
                "Sub_Total": 49,
                "Record_Status__s": "Available",
                "Subject": "301 - Ocultación y ejecución de código Python",
                "$orchestration": false,
                "Contact_Name": null,
                "Locked__s": false,
                "Billing_State": null,
                "$line_tax":
                [],
                "Tag":
                [],
                "$approval_state": "approved",
                "$pathfinder": false,
                "$has_more":
                {
                    "Purchase_Items": false
                }
            }
        ]
    }
    """
    print(response.text)


def refresh():
    # id,user_name,client_id,client_secret,refresh_token,access_token,grant_token,expiry_time,redirect_uri,api_domain
    # 2,,1000.TGMSYJ8A4MIZQ6Z2P0903US5X90OBT,e3f48d0178038efecac049aab2c1455e72adc9c449,1000.c7bab62e9cefd67fe8222376331e7f61.eeffe3e1c1d144315f58d21da1445420,1000.2c501e600446ebf56c4a4093585f2542.3c55c33755c0c28d9ed5f5d3c5e37c1b,1000.a23026ca5cdb217d39b75bc686ebbfdc.cb83ec37a176c86a750a8253403f8364,1731587081871,https://localhost,https://www.zohoapis.eu
    data = {
        "refresh_token": "1000.c7bab62e9cefd67fe8222376331e7f61.eeffe3e1c1d144315f58d21da1445420",
        "client_id": "1000.TGMSYJ8A4MIZQ6Z2P0903US5X90OBT",
        "client_secret": "e3f48d0178038efecac049aab2c1455e72adc9c449",
        "grant_type": "refresh_token"
    }

    url = 'https://accounts.zoho.eu/oauth/v2/token'

    response = requests.post(url, data=data)

    print(response.text)


if __name__ == '__main__':
    # main()
    refresh()
