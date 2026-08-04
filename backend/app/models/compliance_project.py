import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.mixins import TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import ProjectStatus

if TYPE_CHECKING:
    from app.models.compliance_document import ComplianceDocument
    from app.models.compliance_framework import ComplianceFramework
    from app.models.organization import Organization
    from app.models.user import User


class ComplianceProject(
    UUIDPrimaryKeyMixin,
    TimestampMixin,
    Base,
):
    __tablename__ = "compliance_projects"

    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "organizations.id",
            name="fk_compliance_projects_organization_id",
        ),
        nullable=False,
        index=True,
    )

    framework_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "compliance_frameworks.id",
            name="fk_compliance_projects_framework_id",
        ),
        nullable=False,
        index=True,
    )

    created_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "users.id",
            name="fk_compliance_projects_created_by",
        ),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    status: Mapped[ProjectStatus] = mapped_column(
        Enum(
            ProjectStatus,
            name="project_status",
        ),
        nullable=False,
        default=ProjectStatus.DRAFT,
    )

    organization: Mapped["Organization"] = relationship(
        back_populates="compliance_projects",
    )

    framework: Mapped["ComplianceFramework"] = relationship(
        back_populates="compliance_projects",
    )

    creator: Mapped["User"] = relationship(
        back_populates="created_compliance_projects",
    )

    documents: Mapped[list["ComplianceDocument"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
    )