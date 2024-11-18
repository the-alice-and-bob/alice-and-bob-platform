import uuid
import pytest

from alicebob.alicebob_sdk.crm.zoho import ZohoCRM, Lead, LeadNotFoundException


@pytest.fixture
def zoho_crm() -> ZohoCRM:
    return ZohoCRM()


def test_lead_workflow(zoho_crm):
    zoho_leads = zoho_crm.get_leads_module()

    random_email = f"demo{uuid.uuid4()}@example.com"

    print(random_email)

    lead = Lead(
        email=random_email,
        last_name=f"Demo{uuid.uuid4()}",
        first_name=f"Demo{uuid.uuid4()}",
        phone="123456789"
    )

    # Create
    assert zoho_leads.create(lead) is True

    # Get by email
    found_lead = zoho_leads.get_by_email(email=random_email)

    assert found_lead.email == random_email

    # Update
    found_lead.first_name = "Updated"
    assert zoho_leads.update(record_id=found_lead.identifier, **found_lead) is True

    # Get by id
    found_lead = zoho_leads.get_by_id(record_id=found_lead.identifier)

    assert found_lead.first_name == "Updated"

    # Delete
    assert zoho_leads.delete(record_id=found_lead.identifier) is True
    with pytest.raises(LeadNotFoundException):
        zoho_leads.get_by_id(record_id=found_lead.identifier)
