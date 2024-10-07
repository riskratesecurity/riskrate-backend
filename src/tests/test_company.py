import pytest

from riskrate_backend.model.companies import Company


@pytest.fixture
def company_data():
    return {"name": "TechCorp", "registration": "123456789"}


def test_create_company(db_session, company_data):
    company = Company(**company_data)
    db_session.add(company)
    db_session.commit()
    assert company.id is not None
    assert company.name == company_data["name"]
    assert company.registration == company_data["registration"]
