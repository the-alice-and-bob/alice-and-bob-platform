from alicebob.alicebob_sdk.crm.zoho import ZohoCRM, Lead, PurchaseOrder, PurchaseOrderStatus, PurchaseItem
from alicebob_sdk.crm import ProductSummary, Buyer


# ZOHO_CLIENT_ID = "1000.TGMSYJ8A4MIZQ6Z2P0903US5X90OBT"
# ZOHO_CLIENT_SECRET = "e3f48d0178038efecac049aab2c1455e72adc9c449"
# ZOHO_GRANT_TOKEN = "1000.a23026ca5cdb217d39b75bc686ebbfdc.cb83ec37a176c86a750a8253403f8364"

def main():
    crm = ZohoCRM()

    # product_module = crm.get_products_module()
    # for index, product in enumerate(product_module.get_all()):
    #     print(f"{index}: {product}")

    # Purchase orders
    # purchase_orders_module = crm.get_purchase_orders_module()
    #
    # fields = purchase_orders_module.get_module_fields()
    #
    # for f in fields:
    #     print(f)

    # for index, purchase_order in enumerate(purchase_orders_module.get_all()):
    #     print(f"{index}: {purchase_order}")

    # p = purchase_orders_module.get_by_id(738692000001258147)
    #
    # print(p)
    # order = PurchaseOrder(
    #     subject="Test order",
    #     ezycourse_id=10978,
    #     contact_name=Buyer(
    #         identifier=738692000000679037,
    #         name="Test buyer"
    #     ),
    #     status=PurchaseOrderStatus.DELIVERED,
    #     purchase_items=[
    #         PurchaseItem(
    #             description="Test item",
    #             discount=0,
    #             quantity=1,
    #             list_price=100,
    #             total=100,
    #             total_after_discount=100,
    #             tax=0,
    #             product=ProductSummary(
    #                 name="301 - Ocultación y ejecución de código Python",
    #                 identifier=738692000000695355,
    #                 unit_price=100
    #             )
    #         )
    #     ]
    # )
    #
    # print(purchase_orders_module.create(order))

    # for m in crm.get_modules():
    #     print(m)

    # modul_purchase_orders = crm.get_purchase_orders_module()
    # for index, purchase_order in enumerate(modul_purchase_orders.get_all()):
    #     print(f"{index}: {purchase_order}")
    #
    #     if index == 100:
    #         break

    course_progress = crm.get_course_progress_module()
    cp = course_progress.get_by_customer_and_course(customer=738692000001258017, course=738692000000695334)

    course_progress.update(record_id=cp.identifier, Progress=100)

    # print(course_progress.get_by_id(738692000001383012))

    # for index, progress in enumerate(course_progress.get_all()):
    #     print(f"{index}: {progress}")
    #
    #     if index == 100:
    #         break

    # print(lead_module.get_by_email(email="demo83a94196-2c64-4319-9216-2c077a08fe14@example.com"))
    #
    # print("Deleting lead")
    # lead_module.delete(record_id=738692000001441001)
    # print("Lead deleted")

    # lead = None
    #
    # for c in lead_module.get_all():
    #     print(c)
    #     lead = c
    #     break

    # ret = lead_module.get_by_id(lead_id=lead.identifier)
    # print(f"Search by id: {ret}")

    # ret = lead_module.get_by_email(email=lead.email)
    # print(f"Search by email: {ret}")
    # existing_lead = lead_module.get_by_email(email="xxxxxx@xXxxxxxx.com")
    # existing_lead = lead_module.get_by_id(lead_id=738692000009993001)
    # print(existing_lead)


    #
    # lead = Lead(
    #     email="dexxmxodexmo@xXxxxxxx.com",
    #     last_name="Demo",
    #     first_name="Demo000",
    #     phone="123456789"
    # )
    # existing_lead.identifier = existing_lead.identifier + 500
    #
    # lead_module.update(existing_lead.identifier, website="https://www.google.com", phone="123456789")

    # lead_id = lead_module.create(lead)
    #
    # print(f"Lead created: {lead_id}")


    # contacts = crm.get_contacts_modules()
    # for index, contact in enumerate(contacts.get_all()):
    #     print(f"{index}: {contact}")
    #
    #     if index == 100:
    #         break

    # print(lead_module.get_by_email(email="mariaventura1199@outlook.es"))
    # lead_id = lead_module.create(lead)
    # lead = lead_module.get_by_email(email="demo@leading.com")
    #
    # lead.first_name = "Demo2"
    # lead.company = "My new company"
    #
    # lead_module.update(lead)

    # print("Modules:")
    # for module in crm.get_modules():
    #     print(f"  - {module.name}: {module.identifier}")
    #
    # print("Lead module:")
    # leads = crm.get_leads_modules()
    # print(leads.get_by_email(email="mariaventura1199@outlook.es"))
    # print(leads.get_by_id(lead_id=738692000001337001))

    # print("Contacts:")
    # contacts = crm.get_contacts_modules()
    # found = contacts.get_by_email(email="alejandro.sanchez2.tech@bbva.com")
    # found = contacts.get_by_id(contact_id=738692000001271001)


if __name__ == '__main__':
    main()
