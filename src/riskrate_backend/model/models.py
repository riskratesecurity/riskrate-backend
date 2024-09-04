import uuid
from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import JSON
from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

Base = declarative_base()


class BaseMixin:
    id: Mapped[uuid.UUID] = mapped_column(
        PostgresUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )


class CloudType(PyEnum):
    aws = "aws"
    gcp = "gcp"
    azure = "azure"


class Role(Base, BaseMixin):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    users: Mapped[list["User"]] = relationship("User", back_populates="role")


class License(Base, BaseMixin):
    __tablename__ = "licenses"

    code: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String)
    duration: Mapped[int] = mapped_column(Integer)
    features: Mapped[dict] = mapped_column(JSON)

    users: Mapped[list["User"]] = relationship("User", back_populates="license")


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

    partners: Mapped[list["Partner"]] = relationship("Partner", back_populates="user")
    campaigns: Mapped[list["Campaign"]] = relationship(
        "Campaign", back_populates="user"
    )
    user_metrics: Mapped[list["UserMetric"]] = relationship(
        "UserMetric", back_populates="user"
    )
    document_assigns: Mapped[list["DocumentAssign"]] = relationship(
        "DocumentAssign", back_populates="user"
    )
    companies: Mapped[list["CompanyUser"]] = relationship(
        "CompanyUser", back_populates="user"
    )
    cloud_accesses: Mapped[list["CloudAccess"]] = relationship(
        "CloudAccess", back_populates="user"
    )
    cloud_reports: Mapped[list["CloudReport"]] = relationship(
        "CloudReport", back_populates="user"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )


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
    reports: Mapped[list["CloudReport"]] = relationship(
        "CloudReport", back_populates="cloud_access"
    )


class Partner(Base, BaseMixin):
    __tablename__ = "partners"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="partners")


class Campaign(Base, BaseMixin):
    __tablename__ = "campaigns"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="campaigns")


class UserMetric(Base, BaseMixin):
    __tablename__ = "user_metrics"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="user_metrics")


class Company(Base, BaseMixin):
    __tablename__ = "companies"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    registration: Mapped[str] = mapped_column(String(255), nullable=False)
    addresses: Mapped[list["AddressCompany"]] = relationship(
        "AddressCompany", back_populates="company"
    )
    company_users: Mapped[list["CompanyUser"]] = relationship(
        "CompanyUser", back_populates="company"
    )


class Address(Base, BaseMixin):
    __tablename__ = "addresses"

    postcode: Mapped[str] = mapped_column(String(255), nullable=False)
    street: Mapped[str] = mapped_column(String(255), nullable=False)
    number: Mapped[str] = mapped_column(String(255), nullable=False)
    complement: Mapped[str] = mapped_column(String(255))
    neighborhood: Mapped[str] = mapped_column(String(255), nullable=False)
    city: Mapped[str] = mapped_column(String(255), nullable=False)
    state: Mapped[str] = mapped_column(String(255), nullable=False)
    country: Mapped[str] = mapped_column(String(255), nullable=False)


class AddressCompany(Base, BaseMixin):
    __tablename__ = "address_companies"

    address_id: Mapped[int] = mapped_column(ForeignKey("addresses.id"))
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"))

    address: Mapped["Address"] = relationship("Address")
    company: Mapped["Company"] = relationship("Company", back_populates="addresses")


class DocumentAssign(Base, BaseMixin):
    __tablename__ = "document_assigns"

    document_id: Mapped[int] = mapped_column(ForeignKey("assignment_documents.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    document_assignment: Mapped["AssignmentDocument"] = relationship(
        "AssignmentDocument", back_populates="assigns"
    )
    user: Mapped["User"] = relationship("User", back_populates="document_assigns")


class AssignmentDocument(Base, BaseMixin):
    __tablename__ = "assignment_documents"

    code: Mapped[str] = mapped_column(String(255))
    document_slug: Mapped[str] = mapped_column(String(255))
    document_id: Mapped[int] = mapped_column(Integer)
    source: Mapped[str] = mapped_column(String(255))
    assigns: Mapped[list["DocumentAssign"]] = relationship(
        "DocumentAssign", back_populates="document_assignment"
    )
    requests: Mapped[list["AssignmentDocumentRequest"]] = relationship(
        "AssignmentDocumentRequest", back_populates="document_assignment"
    )


class AssignmentDocumentRequest(Base, BaseMixin):
    __tablename__ = "assignment_document_requests"

    document_assignment_id: Mapped[int] = mapped_column(
        ForeignKey("assignment_documents.id")
    )
    status: Mapped[str] = mapped_column(String(255))
    send_to: Mapped[str] = mapped_column(String(255))
    send_to_data: Mapped[dict] = mapped_column(JSON)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    document_assignment: Mapped["AssignmentDocument"] = relationship(
        "AssignmentDocument", back_populates="requests"
    )
    user: Mapped["User"] = relationship("User")


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


class CompanyUser(Base, BaseMixin):
    __tablename__ = "company_users"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"))

    user: Mapped["User"] = relationship("User", back_populates="companies")
    company: Mapped["Company"] = relationship("Company", back_populates="company_users")
