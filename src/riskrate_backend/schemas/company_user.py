from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CompanyUserBase(BaseModel):
    company_id: UUID
    user_id: UUID


class CompanyUserCreate(CompanyUserBase):
    pass


class CompanyUserUpdate(CompanyUserBase):
    pass


class CompanyUser(CompanyUserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
