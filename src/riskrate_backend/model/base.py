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


class Role(Base, BaseMixin):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    users: Mapped[List["User"]] = relationship("User", back_populates="role")


class Partner(Base, BaseMixin):
    __tablename__ = "partners"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="partners")


class Campaign(Base, BaseMixin):
    __tablename__ = "campaigns"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="campaigns")


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
