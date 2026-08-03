import uuid
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    Enum,
    ForeignKey,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.mixins import TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import RequirementSeverity

if TYPE_CHECKING:
    from app.models.compliance_framework import ComplianceFramework


class ComplianceRequirement(
    UUIDPrimaryKeyMixin,
    TimestampMixin,
    Base,
):
    __tablename__ = "compliance_requirements"

    __table_args__ = (
        UniqueConstraint(
            "framework_id",
            "code",
            name="uq_compliance_requirements_framework_code",
        ),
    )

    framework_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "compliance_frameworks.id",
            name="fk_compliance_requirements_framework_id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    code: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    category: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    severity: Mapped[RequirementSeverity] = mapped_column(
        Enum(
            RequirementSeverity,
            name="requirement_severity",
        ),
        nullable=False,
        default=RequirementSeverity.MEDIUM,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    framework: Mapped["ComplianceFramework"] = relationship(
        back_populates="requirements",
    )