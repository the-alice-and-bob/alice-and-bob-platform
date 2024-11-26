"""
This file contains the tasks that are triggered by the EzyCourses webhooks:
"""

from celery import shared_task
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
# @shared_task(name="task_zoho_create_lead")
# def create_zoho_lead(db_lead_id: int):
#     """
#     Create a Zoho Lead
#
#     :param db_lead_id: The ID of the Zoho Lead in the database
#     """
#     pass
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
