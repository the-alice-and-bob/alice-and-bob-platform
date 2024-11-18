from alicebob.alicebob_sdk.crm.zoho import ZohoCRM, Lead


def main():
    ZOHO_CLIENT_ID = "1000.TGMSYJ8A4MIZQ6Z2P0903US5X90OBT"
    ZOHO_CLIENT_SECRET = "e3f48d0178038efecac049aab2c1455e72adc9c449"
    ZOHO_GRANT_TOKEN = "1000.a23026ca5cdb217d39b75bc686ebbfdc.cb83ec37a176c86a750a8253403f8364"
    crm = ZohoCRM(
        zoho_client_id=ZOHO_CLIENT_ID,
        zoho_client_secret=ZOHO_CLIENT_SECRET,
        zoho_grant_token=ZOHO_GRANT_TOKEN,
    )

    # for m in crm.get_modules():
    #     print(m)

    modul_purchase_orders = crm.get_purchase_orders_module()
    for index, purchase_order in enumerate(modul_purchase_orders.get_all()):
        print(f"{index}: {purchase_order}")

        if index == 100:
            break

    # lead_module = crm.get_leads_module()
    #
    # c = 0
    # for lead in lead_module.get_all():
    #     print(lead)
    #
    #     c += 1
    #
    #     if c == 85:
    #         break

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
