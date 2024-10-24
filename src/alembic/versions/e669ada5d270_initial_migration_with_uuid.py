"""Initial migration with UUID

Revision ID: e669ada5d270
Revises: 
Create Date: 2024-08-30 09:59:43.800263

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e669ada5d270"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "addresses",
        sa.Column("postcode", sa.String(length=255), nullable=False),
        sa.Column("street", sa.String(length=255), nullable=False),
        sa.Column("number", sa.String(length=255), nullable=False),
        sa.Column("complement", sa.String(length=255), nullable=False),
        sa.Column("neighborhood", sa.String(length=255), nullable=False),
        sa.Column("city", sa.String(length=255), nullable=False),
        sa.Column("state", sa.String(length=255), nullable=False),
        sa.Column("country", sa.String(length=255), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "assignment_documents",
        sa.Column("code", sa.String(length=255), nullable=False),
        sa.Column("document_slug", sa.String(length=255), nullable=False),
        sa.Column("document_id", sa.Integer(), nullable=False),
        sa.Column("source", sa.String(length=255), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "companies",
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("registration", sa.String(length=255), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "licenses",
        sa.Column("code", sa.String(length=255), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("duration", sa.Integer(), nullable=False),
        sa.Column("features", sa.JSON(), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "address_companies",
        sa.Column("address_id", sa.UUID(), nullable=False),
        sa.Column("company_id", sa.UUID(), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["address_id"],
            ["addresses.id"],
        ),
        sa.ForeignKeyConstraint(
            ["company_id"],
            ["companies.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "users",
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("role_id", sa.Integer(), nullable=False),
        sa.Column("license_id", sa.UUID(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("position", sa.String(length=255), nullable=False),
        sa.Column("nationality", sa.String(length=255), nullable=False),
        sa.Column("marital_state", sa.String(length=255), nullable=False),
        sa.Column("government_registration", sa.String(length=255), nullable=False),
        sa.Column("issuing_department_state", sa.String(length=255), nullable=False),
        sa.Column("issuing_department", sa.String(length=255), nullable=False),
        sa.Column("personal_registration", sa.String(length=255), nullable=False),
        sa.Column("password", sa.String(length=255), nullable=False),
        sa.Column("remember_me_token", sa.String(length=255), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["license_id"],
            ["licenses.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "assignment_document_requests",
        sa.Column("document_assignment_id", sa.UUID(), nullable=False),
        sa.Column("status", sa.String(length=255), nullable=False),
        sa.Column("send_to", sa.String(length=255), nullable=False),
        sa.Column("send_to_data", sa.JSON(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["document_assignment_id"],
            ["assignment_documents.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "cloud_accesses",
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column(
            "cloud", sa.Enum("aws", "gcp", "azure", name="cloudtype"), nullable=False
        ),
        sa.Column("access_key", sa.String(length=255), nullable=False),
        sa.Column("tenant_id", sa.String(length=255), nullable=False),
        sa.Column("secret_key", sa.String(length=255), nullable=False),
        sa.Column("shadow_access_key", sa.String(length=255), nullable=False),
        sa.Column("region", sa.String(length=255), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "document_assigns",
        sa.Column("document_id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["document_id"],
            ["assignment_documents.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "cloud_reports",
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("cloud_access_id", sa.UUID(), nullable=False),
        sa.Column("status", sa.String(length=255), nullable=False),
        sa.Column("message", sa.String(), nullable=False),
        sa.Column("report_file", sa.String(length=255), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["cloud_access_id"],
            ["cloud_accesses.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("cloud_reports")
    op.drop_table("document_assigns")
    op.drop_table("cloud_accesses")
    op.drop_table("assignment_document_requests")
    op.drop_table("users")
    op.drop_table("address_companies")
    op.drop_table("licenses")
    op.drop_table("companies")
    op.drop_table("assignment_documents")
    op.drop_table("addresses")
    # ### end Alembic commands ###
