from typing import List

from sqlalchemy import JSON
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from riskrate_backend.model.base import Base, BaseMixin, Address

class Company(Base, BaseMixin):
    __tablename__ = "companies"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    registration: Mapped[str] = mapped_column(String(255), nullable=False)
    addresses: Mapped[List["AddressCompany"]] = relationship(
        "AddressCompany", back_populates="company"
    )
    company_users: Mapped[List["CompanyUser"]] = relationship(
        "CompanyUser", back_populates="company"
    )


class AddressCompany(Base, BaseMixin):
    __tablename__ = "address_companies"

    address_id: Mapped[int] = mapped_column(ForeignKey("addresses.id"))
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"))

    address: Mapped["Address"] = relationship("Address")
    company: Mapped["Company"] = relationship("Company", back_populates="addresses")


class CompanyUser(Base, BaseMixin):
    __tablename__ = "company_users"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"))

    user: Mapped["User"] = relationship("User", back_populates="companies")
    company: Mapped["Company"] = relationship("Company", back_populates="company_users")
