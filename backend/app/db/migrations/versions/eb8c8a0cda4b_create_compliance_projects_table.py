"""create compliance projects table

Revision ID: eb8c8a0cda4b
Revises: 8df714eddf04
Create Date: 2026-08-03 17:52:54.809246
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "eb8c8a0cda4b"
down_revision: Union[str, Sequence[str], None] = "8df714eddf04"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


project_status_enum = postgresql.ENUM(
    "DRAFT",
    "IN_REVIEW",
    "COMPLETED",
    "ARCHIVED",
    name="project_status",
    create_type=False,
)


def upgrade() -> None:
    """Upgrade schema."""

    project_status_enum.create(
        op.get_bind(),
        checkfirst=True,
    )

    op.create_table(
        "compliance_projects",
        sa.Column(
            "organization_id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "framework_id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "created_by",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "name",
            sa.String(length=255),
            nullable=False,
        ),
        sa.Column(
            "description",
            sa.Text(),
            nullable=True,
        ),
        sa.Column(
            "status",
            project_status_enum,
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
            ["created_by"],
            ["users.id"],
            name="fk_compliance_projects_created_by",
        ),
        sa.ForeignKeyConstraint(
            ["framework_id"],
            ["compliance_frameworks.id"],
            name="fk_compliance_projects_framework_id",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organizations.id"],
            name="fk_compliance_projects_organization_id",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_compliance_projects_created_by"),
        "compliance_projects",
        ["created_by"],
        unique=False,
    )

    op.create_index(
        op.f("ix_compliance_projects_framework_id"),
        "compliance_projects",
        ["framework_id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_compliance_projects_organization_id"),
        "compliance_projects",
        ["organization_id"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(
        op.f("ix_compliance_projects_organization_id"),
        table_name="compliance_projects",
    )

    op.drop_index(
        op.f("ix_compliance_projects_framework_id"),
        table_name="compliance_projects",
    )

    op.drop_index(
        op.f("ix_compliance_projects_created_by"),
        table_name="compliance_projects",
    )

    op.drop_table("compliance_projects")

    project_status_enum.drop(
        op.get_bind(),
        checkfirst=True,
    )