"""create compliance requirements table

Revision ID: 8df714eddf04
Revises: 1ed865d8cdb7
Create Date: 2026-08-03 17:38:05.415275
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "8df714eddf04"
down_revision: Union[str, Sequence[str], None] = "1ed865d8cdb7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


requirement_severity_enum = postgresql.ENUM(
    "LOW",
    "MEDIUM",
    "HIGH",
    "CRITICAL",
    name="requirement_severity",
    create_type=False,
)


def upgrade() -> None:
    """Upgrade schema."""

    requirement_severity_enum.create(
        op.get_bind(),
        checkfirst=True,
    )

    op.create_table(
        "compliance_requirements",
        sa.Column(
            "framework_id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "code",
            sa.String(length=100),
            nullable=False,
        ),
        sa.Column(
            "title",
            sa.String(length=255),
            nullable=False,
        ),
        sa.Column(
            "description",
            sa.Text(),
            nullable=False,
        ),
        sa.Column(
            "category",
            sa.String(length=100),
            nullable=True,
        ),
        sa.Column(
            "severity",
            requirement_severity_enum,
            nullable=False,
        ),
        sa.Column(
            "is_active",
            sa.Boolean(),
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
            ["framework_id"],
            ["compliance_frameworks.id"],
            name="fk_compliance_requirements_framework_id",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "framework_id",
            "code",
            name="uq_compliance_requirements_framework_code",
        ),
    )

    op.create_index(
        op.f("ix_compliance_requirements_framework_id"),
        "compliance_requirements",
        ["framework_id"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(
        op.f("ix_compliance_requirements_framework_id"),
        table_name="compliance_requirements",
    )

    op.drop_table("compliance_requirements")

    requirement_severity_enum.drop(
        op.get_bind(),
        checkfirst=True,
    )