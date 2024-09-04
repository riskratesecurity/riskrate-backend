from datetime import datetime
from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException

from riskrate_backend.schemas.address import Address, AddressCreate, AddressUpdate

router = APIRouter()

# Dados em memória
addresses = []


@router.post("/", response_model=Address)
def create_address(address: AddressCreate):
    new_address = Address(
        id=uuid4(),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        **address.dict()
    )
    addresses.append(new_address)
    return new_address


@router.get("/{address_id}", response_model=Address)
def get_address(address_id: UUID):
    address = next((addr for addr in addresses if addr.id == address_id), None)
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    return address


@router.put("/{address_id}", response_model=Address)
def update_address(address_id: UUID, address: AddressUpdate):
    existing_address = next((addr for addr in addresses if addr.id == address_id), None)
    if not existing_address:
        raise HTTPException(status_code=404, detail="Address not found")

    updated_data = address.dict(exclude_unset=True)
    for key, value in updated_data.items():
        setattr(existing_address, key, value)
    existing_address.updated_at = datetime.utcnow()
    return existing_address


@router.delete("/{address_id}")
def delete_address(address_id: UUID):
    global addresses
    addresses = [addr for addr in addresses if addr.id != address_id]
    return {"detail": "Address deleted successfully"}
