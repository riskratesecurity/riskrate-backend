from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel


class LicenseBase(BaseModel):
    code: str
    name: str
    description: str
    duration: int
    features: List[str]


class LicenseCreate(LicenseBase):
    pass


class LicenseUpdate(LicenseBase):
    pass


class License(LicenseBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
