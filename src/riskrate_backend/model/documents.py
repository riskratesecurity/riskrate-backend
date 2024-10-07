from sqlalchemy import JSON
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from base import Base
from base import BaseMixin


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
