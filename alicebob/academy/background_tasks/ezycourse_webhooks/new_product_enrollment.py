from django.db.transaction import atomic

from alicebob_sdk import zoho_instance
from awesome_zohocrm import ZohoCRM, Contact, ContactNotFoundException, Lead

from .helpers import *

from .models import NewProduct


def ezycourse_new_product_enrollment(data: dict):
    """
    This webhook is triggered when a new user signs up.
    """
    try:
        obj = NewProduct.from_json(data)
    except Exception as e:
        raise ValueError(f"Invalid data: {e}")

    zoho: ZohoCRM = zoho_instance()

    try:
        st = check_or_create_student(
            email=obj.email,
            identifier=obj.identifier,
            first_name=obj.first_name,
            last_name=obj.last_name,
            zoho=zoho,
        )
    except Exception as e:
        print(f"Error creating student: {e}")
        return False

    # Now we have to get the product ID
    with atomic():

        #
        # Local DB changes
        #
        pd = get_or_create_product(zoho, obj.product_id, obj.product_name, obj.price, obj.product_type)

        # -------------------------------------------------------------------------
        # This is the most important part of the code. Manage Leads / Contacts
        # -------------------------------------------------------------------------
        # If not ezy_id in student, populate with Zoho ID
        if st.zoho_id is None:
            zoho_id, is_lead = get_contact_or_lead(st.email, zoho)

            if zoho_id:
                st.zoho_id = zoho_id
                st.zoho_is_lead = is_lead
                st.save()

        # At this point it means that there are no Leads or Contacts in Zoho for this student. So we have to create a Lead
        if st.zoho_id is None:
            print(f"Student {obj.identifier} not found in Zoho. Creating Lead...")
            zoho_lead_module = load_module_and_cache(zoho, "get_leads_module")

            zoho_lead_id = zoho_lead_module.create(Lead(
                email=st.email,
                first_name=st.first_name,
                last_name=st.last_name,
            ))

            st.zoho_id = zoho_lead_id
            st.zoho_is_lead = True
            st.save()

        get_or_create_purchase_order(zoho, st, pd, gateway=obj.gateway, update_zoho=False)

        # -------------------------------------------------------------------------
        # Update user tags
        # -------------------------------------------------------------------------
        update_user_tags(zoho, st, pd, lead_or_contact="lead")


__all__ = ("ezycourse_new_product_enrollment",)
