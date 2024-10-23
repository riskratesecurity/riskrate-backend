from sqlalchemy import JSON, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import List

from riskrate_backend.model.base import Base, BaseMixin


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
    assigns: Mapped[List["DocumentAssign"]] = relationship(
        "DocumentAssign", back_populates="document_assignment"
    )
    requests: Mapped[List["AssignmentDocumentRequest"]] = relationship(
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
