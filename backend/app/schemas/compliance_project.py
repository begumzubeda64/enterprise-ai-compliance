from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import ProjectStatus


class ComplianceProjectCreate(BaseModel):
    framework_id: UUID

    name: str = Field(
        min_length=2,
        max_length=255,
    )

    description: str | None = Field(
        default=None,
        max_length=2000,
    )


class ComplianceProjectResponse(BaseModel):
    id: UUID
    organization_id: UUID
    framework_id: UUID
    created_by: UUID
    name: str
    description: str | None
    status: ProjectStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )