from typing import TYPE_CHECKING

from sqlalchemy import Boolean, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.mixins import TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.compliance_project import ComplianceProject
    from app.models.compliance_requirement import ComplianceRequirement


class ComplianceFramework(
    UUIDPrimaryKeyMixin,
    TimestampMixin,
    Base,
):
    __tablename__ = "compliance_frameworks"

    __table_args__ = (
        UniqueConstraint(
            "name",
            "version",
            name="uq_compliance_frameworks_name_version",
        ),
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    version: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    requirements: Mapped[list["ComplianceRequirement"]] = relationship(
        back_populates="framework",
        cascade="all, delete-orphan",
    )

    compliance_projects: Mapped[list["ComplianceProject"]] = relationship(
        back_populates="framework",
    )