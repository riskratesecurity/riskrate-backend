import pytest

from riskrate_backend.model.models import Address


@pytest.fixture
def address_data():
    return {
        "postcode": "12345-678",
        "street": "Main St",
        "number": "100",
        "complement": "Apt 101",
        "neighborhood": "Downtown",
        "city": "Metropolis",
        "state": "SP",
        "country": "Brazil",
    }


def test_create_address(db_session, address_data):
    address = Address(**address_data)
    db_session.add(address)
    db_session.commit()
    assert address.id is not None
    assert address.postcode == address_data["postcode"]
    assert address.street == address_data["street"]
    assert address.number == address_data["number"]
    assert address.complement == address_data["complement"]
    assert address.neighborhood == address_data["neighborhood"]
    assert address.city == address_data["city"]
    assert address.state == address_data["state"]
    assert address.country == address_data["country"]
    assert address.state == address_data["state"]
    assert address.country == address_data["country"]
