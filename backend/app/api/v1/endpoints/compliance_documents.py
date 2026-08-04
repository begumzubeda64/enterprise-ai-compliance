from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
    status,
)

from app.auth.authorization import require_roles
from app.auth.dependencies import get_current_user
from app.dependencies.services import (
    get_compliance_document_service,
)
from app.models.enums import UserRole
from app.models.user import User
from app.schemas.common.pagination import (
    PaginatedResponse,
    PaginationParams,
)
from app.schemas.compliance_document import (
    ComplianceDocumentDownloadResponse,
    ComplianceDocumentResponse,
)
from app.services.compliance_document_service import (
    ComplianceDocumentService,
)

router = APIRouter(
    prefix="/projects/{project_id}/documents",
    tags=["Compliance Documents"],
)


@router.post(
    "",
    response_model=ComplianceDocumentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload Compliance Document",
)
async def upload_document(
    project_id: UUID,
    file: UploadFile = File(...),
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.REVIEWER,
            UserRole.USER,
        )
    ),
    service: ComplianceDocumentService = Depends(
        get_compliance_document_service
    ),
) -> ComplianceDocumentResponse:
    """
    Upload a compliance document to Amazon S3 and save its
    metadata against the selected compliance project.
    """

    return await service.upload_document(
        project_id=project_id,
        file=file,
        current_user=current_user,
    )


@router.get(
    "",
    response_model=PaginatedResponse[
        ComplianceDocumentResponse
    ],
    summary="List Compliance Documents",
)
async def list_documents(
    project_id: UUID,
    pagination: PaginationParams = Depends(),
    current_user: User = Depends(get_current_user),
    service: ComplianceDocumentService = Depends(
        get_compliance_document_service
    ),
) -> PaginatedResponse[
    ComplianceDocumentResponse
]:
    """
    List documents belonging to a compliance project in the
    authenticated user's organization.
    """

    return await service.list_documents(
        project_id=project_id,
        pagination=pagination,
        current_user=current_user,
    )


@router.get(
    "/{document_id}/download",
    response_model=ComplianceDocumentDownloadResponse,
    summary="Generate Document Download URL",
)
async def generate_document_download_url(
    project_id: UUID,
    document_id: UUID,
    current_user: User = Depends(get_current_user),
    service: ComplianceDocumentService = Depends(
        get_compliance_document_service
    ),
) -> ComplianceDocumentDownloadResponse:
    """
    Generate a temporary presigned S3 URL for downloading
    an authorized compliance document.
    """

    expires_in_seconds = 900

    download_url = (
        await service.get_document_download_url(
            project_id=project_id,
            document_id=document_id,
            current_user=current_user,
        )
    )

    return ComplianceDocumentDownloadResponse(
        download_url=download_url,
        expires_in_seconds=expires_in_seconds,
    )