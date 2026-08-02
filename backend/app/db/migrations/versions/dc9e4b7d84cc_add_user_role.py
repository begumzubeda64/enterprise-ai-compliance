"""add user role

Revision ID: dc9e4b7d84cc
Revises: 12161a18422a
Create Date: 2026-08-02 21:53:40.461143
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "dc9e4b7d84cc"
down_revision: Union[str, Sequence[str], None] = "12161a18422a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


user_role = sa.Enum(
    "ADMIN",
    "REVIEWER",
    "AUDITOR",
    "USER",
    name="user_role",
)


def upgrade() -> None:
    """Upgrade schema."""

    # Create PostgreSQL enum type
    user_role.create(op.get_bind(), checkfirst=True)

    # Add column with default for existing rows
    op.add_column(
        "users",
        sa.Column(
            "role",
            user_role,
            nullable=False,
            server_default="USER",
        ),
    )

    # Remove default so future inserts use SQLAlchemy model default
    op.alter_column(
        "users",
        "role",
        server_default=None,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column("users", "role")

    user_role.drop(op.get_bind(), checkfirst=True)