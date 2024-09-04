import pytest
from riskrate_backend.model.models import (
    CloudType,
    User,
    Role,
    License,
    Company,
    CloudAccess,
)


@pytest.fixture
def user_data():
    return {
        "name": "John Doe",
        "email": "johndoe@example.com",
        "position": "Engineer",
        "nationality": "American",
        "marital_state": "Single",
        "government_registration": "123456789",
        "issuing_department_state": "NY",
        "issuing_department": "NY Dept",
        "personal_registration": "987654321",
        "password": "securepassword",
        "remember_me_token": None,
    }


@pytest.fixture
def role(db_session):
    role = Role(name="Admin", description="Administrator role")
    db_session.add(role)
    db_session.commit()
    return role


@pytest.fixture
def license(db_session):
    license = License(
        code="LIC123",
        name="Standard License",
        description="A standard license",
        duration=365,
        features={"feature1": True, "feature2": False},
    )
    db_session.add(license)
    db_session.commit()
    return license


@pytest.fixture
def company(db_session):
    company = Company(
        name="ACME Corp",
        registration="123456789",
    )
    db_session.add(company)
    db_session.commit()
    return company


def test_create_user(db_session, user_data, role, license, company):
    user_data["role_id"] = role.id
    user_data["license_id"] = license.id

    user = User(**user_data)
    db_session.add(user)
    db_session.commit()

    assert user.id is not None
    assert user.name == user_data["name"]
    assert user.email == user_data["email"]
    assert user.role_id == role.id
    assert user.license_id == license.id
    assert user.role.name == "Admin"
    assert user.license.name == "Standard License"


def test_user_cloud_access(db_session, user_data, role):
    user_data["role_id"] = role.id
    user = User(**user_data)
    db_session.add(user)
    db_session.commit()

    cloud_access = CloudAccess(
        user_id=user.id,
        name="AWS Access",
        cloud=CloudType.aws,
        access_key="ACCESS_KEY",
        tenant_id="TENANT_ID",
        secret_key="SECRET_KEY",
        shadow_access_key="SHADOW_KEY",
        region="us-east-1",
    )
    db_session.add(cloud_access)
    db_session.commit()

    assert cloud_access.id is not None
    assert cloud_access.user_id == user.id
    assert cloud_access.user.name == user.name
    assert cloud_access.cloud == CloudType.aws
