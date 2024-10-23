import uuid
from datetime import datetime
from enum import Enum as PyEnum

from typing import List

from sqlalchemy import JSON
from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from riskrate_backend.model.base import Base, BaseMixin, Role, Partner, Campaign
from riskrate_backend.model.documents import DocumentAssign
from riskrate_backend.model.companies import CompanyUser

class User(Base, BaseMixin):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        PostgresUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    role_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("roles.id"), nullable=False)
    license_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("licenses.id"), nullable=True
    )
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    position: Mapped[str] = mapped_column(String(255))
    nationality: Mapped[str] = mapped_column(String(255))
    marital_state: Mapped[str] = mapped_column(String(255))
    government_registration: Mapped[str] = mapped_column(String(255))
    issuing_department_state: Mapped[str] = mapped_column(String(255))
    issuing_department: Mapped[str] = mapped_column(String(255))
    personal_registration: Mapped[str] = mapped_column(String(255))
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    remember_me_token: Mapped[str] = mapped_column(String(255), nullable=True)

    role: Mapped["Role"] = relationship("Role", back_populates="users")
    license: Mapped["License"] = relationship("License", back_populates="users")

    partners: Mapped[List["Partner"]] = relationship("Partner", back_populates="user")
    campaigns: Mapped[List["Campaign"]] = relationship(
        "Campaign", back_populates="user"
    )
    user_metrics: Mapped[List["UserMetric"]] = relationship(
        "UserMetric", back_populates="user"
    )
    document_assigns: Mapped[List["DocumentAssign"]] = relationship(
        "DocumentAssign", back_populates="user"
    )
    companies: Mapped[List["CompanyUser"]] = relationship(
        "CompanyUser", back_populates="user"
    )
    cloud_accesses: Mapped[List["CloudAccess"]] = relationship(
        "CloudAccess", back_populates="user"
    )
    cloud_reports: Mapped[List["CloudReport"]] = relationship(
        "CloudReport", back_populates="user"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )


class UserMetric(Base, BaseMixin):
    __tablename__ = "user_metrics"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="user_metrics")


class License(Base, BaseMixin):
    __tablename__ = "licenses"

    code: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String)
    duration: Mapped[int] = mapped_column(Integer)
    features: Mapped[dict] = mapped_column(JSON)

    users: Mapped[List["User"]] = relationship("User", back_populates="license")


class CloudType(PyEnum):
    aws = "aws"
    gcp = "gcp"
    azure = "azure"


class CloudAccess(Base, BaseMixin):
    __tablename__ = "cloud_accesses"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(String(255))
    cloud: Mapped[CloudType] = mapped_column(Enum(CloudType))
    access_key: Mapped[str] = mapped_column(String(255))
    tenant_id: Mapped[str] = mapped_column(String(255))
    secret_key: Mapped[str] = mapped_column(String(255))
    shadow_access_key: Mapped[str] = mapped_column(String(255))
    region: Mapped[str] = mapped_column(String(255))

    # Relacionamentos
    user: Mapped["User"] = relationship("User", back_populates="cloud_accesses")
    reports: Mapped[List["CloudReport"]] = relationship(
        "CloudReport", back_populates="cloud_access"
    )


class CloudReport(Base, BaseMixin):
    __tablename__ = "cloud_reports"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    cloud_access_id: Mapped[int] = mapped_column(ForeignKey("cloud_accesses.id"))
    status: Mapped[str] = mapped_column(String(255))
    message: Mapped[str] = mapped_column(String)
    report_file: Mapped[str] = mapped_column(String(255))

    user: Mapped["User"] = relationship("User")
    cloud_access: Mapped["CloudAccess"] = relationship(
        "CloudAccess", back_populates="reports"
    )
