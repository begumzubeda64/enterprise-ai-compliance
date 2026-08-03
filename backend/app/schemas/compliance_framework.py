from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ComplianceFrameworkResponse(BaseModel):
    id: UUID
    name: str
    version: str
    description: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )