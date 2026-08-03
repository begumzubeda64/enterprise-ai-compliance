from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.schemas.user import UserResponse


class OrganizationOnboardRequest(BaseModel):
    organization_name: str = Field(
        min_length=2,
        max_length=255,
    )

    organization_slug: str = Field(
        min_length=2,
        max_length=100,
        pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
    )

    organization_description: str | None = Field(
        default=None,
        max_length=2000,
    )

    admin_full_name: str = Field(
        min_length=2,
        max_length=255,
    )

    admin_email: EmailStr

    admin_password: str = Field(
        min_length=8,
        max_length=128,
    )


class OrganizationResponse(BaseModel):
    id: UUID
    name: str
    slug: str
    description: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OrganizationOnboardResponse(BaseModel):
    organization: OrganizationResponse
    admin: UserResponse