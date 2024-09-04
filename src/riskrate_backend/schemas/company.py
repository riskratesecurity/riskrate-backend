from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from .address import Address


class CompanyBase(BaseModel):
    name: str
    registration: str


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(CompanyBase):
    pass


class Company(CompanyBase):
    id: UUID
    addresses: list[Address] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
