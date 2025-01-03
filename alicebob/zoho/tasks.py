"""
This file contains the tasks that are triggered by the EzyCourses webhooks:
"""
from awesome_zohocrm import ZohoCRM, ZohoLeads as ZohoLeadModule, Lead

from celery import shared_task
from zoho.sdk import zoho_instance
from zoho.models import ZohoLead


@shared_task(name="task_zoho_create_lead")
def create_zoho_lead(db_lead_id: int):
    """
    Create a Zoho Lead

    :param db_lead_id: The ID of the Zoho Lead in the database
    """
    crm: ZohoCRM = zoho_instance()
    leads_module: ZohoLeadModule = crm.get_leads_module()

    try:
        lead_obj = ZohoLead.objects.get(id=db_lead_id)
    except ZohoLead.DoesNotExist:
        print(f"Zoho Lead with ID {db_lead_id} does not exist")
        return

    lead_id = leads_module.create(Lead(
        email=lead_obj.student.email,
        last_name=lead_obj.student.last_name,
        first_name=lead_obj.student.first_name,
        ezycourse_id=lead_obj.student.ezy_id
    ))

    # Update the Zoho Lead with the new ID
    lead_obj.lead_id = lead_id
    lead_obj.save()

#
#
# @shared_task(name="task_zoho_create_tag")
# def create_zoho_tag(db_tag_id: int):
#     """
#     Create a Zoho Tag
#
#     :param db_tag_id: The ID of the Zoho Tag in the database
#     """
#     pass
#
#
# @shared_task(name="task_zoho_create_product")
# def create_zoho_product(db_product_id: int):
#     """
#     Create a Zoho Product
#
#     :param db_product_id: The ID of the Zoho Product in the database
#     """
#     pass
#
#

#
# @shared_task(name="task_zoho_create_contact")
# def create_zoho_contact(db_contact_id: int):
#     """
#     Create a Zoho Contact
#
#     :param db_contact_id: The ID of the Zoho Contact in the database
#     """
#     pass
#
#
# @shared_task(name="task_zoho_create_purchase_order")
# def create_zoho_purchase_order(db_purchase_order_id: int):
#     """
#     Create a Zoho Purchase Order
#
#     :param db_purchase_order_id: The ID of the Zoho Purchase Order in the database
#     """
#     pass
