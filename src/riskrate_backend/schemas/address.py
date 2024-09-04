from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class AddressBase(BaseModel):
    postcode: str
    street: str
    number: str
    complement: str
    neighborhood: str
    city: str
    state: str
    country: str


class AddressCreate(AddressBase):
    pass


class AddressUpdate(AddressBase):
    pass


class Address(AddressBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
