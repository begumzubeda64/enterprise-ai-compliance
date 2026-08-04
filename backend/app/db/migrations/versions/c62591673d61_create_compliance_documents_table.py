"""create compliance documents table

Revision ID: c62591673d61
Revises: eb8c8a0cda4b
Create Date: 2026-08-04 20:04:56.282726
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "c62591673d61"
down_revision: Union[str, Sequence[str], None] = "eb8c8a0cda4b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


document_status_enum = postgresql.ENUM(
    "UPLOADED",
    "EXTRACTING",
    "READY",
    "FAILED",
    name="document_status",
    create_type=False,
)


def upgrade() -> None:
    """Upgrade schema."""

    document_status_enum.create(
        op.get_bind(),
        checkfirst=True,
    )

    op.create_table(
        "compliance_documents",
        sa.Column(
            "project_id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "uploaded_by",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "original_filename",
            sa.String(length=255),
            nullable=False,
        ),
        sa.Column(
            "stored_filename",
            sa.String(length=255),
            nullable=False,
        ),
        sa.Column(
            "mime_type",
            sa.String(length=255),
            nullable=False,
        ),
        sa.Column(
            "file_size",
            sa.BigInteger(),
            nullable=False,
        ),
        sa.Column(
            "checksum",
            sa.String(length=64),
            nullable=False,
        ),
        sa.Column(
            "storage_key",
            sa.String(length=1024),
            nullable=False,
        ),
        sa.Column(
            "status",
            document_status_enum,
            nullable=False,
        ),
        sa.Column(
            "id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["compliance_projects.id"],
            name="fk_compliance_documents_project_id",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["uploaded_by"],
            ["users.id"],
            name="fk_compliance_documents_uploaded_by",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "storage_key",
            name="uq_compliance_documents_storage_key",
        ),
    )

    op.create_index(
        op.f("ix_compliance_documents_project_id"),
        "compliance_documents",
        ["project_id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_compliance_documents_uploaded_by"),
        "compliance_documents",
        ["uploaded_by"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(
        op.f("ix_compliance_documents_uploaded_by"),
        table_name="compliance_documents",
    )

    op.drop_index(
        op.f("ix_compliance_documents_project_id"),
        table_name="compliance_documents",
    )

    op.drop_table("compliance_documents")

    document_status_enum.drop(
        op.get_bind(),
        checkfirst=True,
    )