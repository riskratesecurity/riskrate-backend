from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    name: str
    role_id: int
    email: EmailStr
    position: str
    nationality: str
    marital_state: str
    government_registration: str
    issuing_department_state: str
    issuing_department: str
    personal_registration: str


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    pass


class User(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
