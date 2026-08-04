from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.enums import DocumentStatus


class ComplianceDocumentResponse(BaseModel):
    id: UUID
    project_id: UUID
    uploaded_by: UUID
    original_filename: str
    mime_type: str
    file_size: int
    status: DocumentStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class ComplianceDocumentDownloadResponse(BaseModel):
    download_url: str
    expires_in_seconds: int