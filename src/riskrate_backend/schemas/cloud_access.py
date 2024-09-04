from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class CloudTypeEnum(str, Enum):
    aws = "aws"
    gcp = "gcp"
    azure = "azure"


class CloudAccessBase(BaseModel):
    name: str
    cloud: CloudTypeEnum
    access_key: str
    tenant_id: str
    secret_key: str
    shadow_access_key: str
    region: str


class CloudAccessCreate(CloudAccessBase):
    pass


class CloudAccessUpdate(CloudAccessBase):
    pass


class CloudAccess(CloudAccessBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
