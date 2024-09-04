from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class AssignmentDocumentBase(BaseModel):
    code: str
    document_slug: str
    document_id: int
    source: str


class AssignmentDocumentCreate(AssignmentDocumentBase):
    pass


class AssignmentDocumentUpdate(AssignmentDocumentBase):
    pass


class AssignmentDocument(AssignmentDocumentBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
