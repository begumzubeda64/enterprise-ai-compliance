import traceback
import uuid
from uuid import UUID

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.tenant import get_user_organization_id
from app.exceptions.compliance_document import (
    ComplianceDocumentNotFoundException,
)
from app.exceptions.compliance_project import (
    ComplianceProjectNotFoundException,
)
from app.models.compliance_document import ComplianceDocument
from app.models.enums import DocumentStatus
from app.models.user import User
from app.repositories.compliance_document_repository import (
    ComplianceDocumentRepository,
)
from app.repositories.compliance_project_repository import (
    ComplianceProjectRepository,
)
from app.schemas.common.pagination import (
    PaginatedResponse,
    PaginationParams,
)
from app.schemas.compliance_document import (
    ComplianceDocumentResponse,
)
from app.services.document_processing_service import (
    DocumentProcessingService,
)
from app.storage.base import BaseStorageService


class ComplianceDocumentService:
    """
    Manages compliance-document uploads and metadata.
    """

    def __init__(
        self,
        document_repository: ComplianceDocumentRepository,
        project_repository: ComplianceProjectRepository,
        processing_service: DocumentProcessingService,
        storage_service: BaseStorageService,
        db: AsyncSession,
    ):
        self.document_repository = document_repository
        self.project_repository = project_repository
        self.processing_service = processing_service
        self.storage_service = storage_service
        self.db = db

    async def upload_document(
        self,
        *,
        project_id: UUID,
        file: UploadFile,
        current_user: User,
    ) -> ComplianceDocumentResponse:
        organization_id = get_user_organization_id(
            current_user
        )

        project = (
            await self.project_repository
            .get_by_id_and_organization(
                project_id=project_id,
                organization_id=organization_id,
            )
        )

        if project is None:
            raise ComplianceProjectNotFoundException(
                project_id
            )

        extension = (
            self.processing_service.validate_file_type(
                file
            )
        )

        file_size = (
            await self.processing_service.get_file_size(
                file
            )
        )

        checksum = (
            await self.processing_service.calculate_sha256(
                file
            )
        )

        document_id = uuid.uuid4()

        stored_filename = (
            self.storage_service.generate_stored_filename(
                document_id=document_id,
                extension=extension,
            )
        )

        storage_key = (
            self.storage_service.build_document_storage_key(
                organization_id=organization_id,
                project_id=project.id,
                document_id=document_id,
                stored_filename=stored_filename,
            )
        )

        mime_type = (
            file.content_type
            or "application/octet-stream"
        )

        uploaded_to_storage = False

        try:
            await file.seek(0)

            await self.storage_service.upload_file(
                file=file.file,
                object_key=storage_key,
                content_type=mime_type,
                metadata={
                    "organization-id": str(organization_id),
                    "project-id": str(project.id),
                    "document-id": str(document_id),
                    "uploaded-by": str(current_user.id),
                    "checksum": checksum,
                },
            )

            uploaded_to_storage = True

            document = ComplianceDocument(
                id=document_id,
                project_id=project.id,
                uploaded_by=current_user.id,
                original_filename=(
                    file.filename or stored_filename
                ),
                stored_filename=stored_filename,
                mime_type=mime_type,
                file_size=file_size,
                checksum=checksum,
                storage_key=storage_key,
                status=DocumentStatus.UPLOADED,
            )

            created_document = (
                await self.document_repository.create(
                    document
                )
            )

            response = (
                ComplianceDocumentResponse.model_validate(
                    created_document
                )
            )

            await self.db.commit()

            return response

        except Exception:
            await self.db.rollback()

            if uploaded_to_storage:
                try:
                    await self.storage_service.delete_file(
                        storage_key
                    )
                except Exception:
                    pass

            traceback.print_exc()
            raise

        finally:
            await file.close()

    async def list_documents(
        self,
        *,
        project_id: UUID,
        pagination: PaginationParams,
        current_user: User,
    ) -> PaginatedResponse[
        ComplianceDocumentResponse
    ]:
        organization_id = get_user_organization_id(
            current_user
        )

        project = (
            await self.project_repository
            .get_by_id_and_organization(
                project_id=project_id,
                organization_id=organization_id,
            )
        )

        if project is None:
            raise ComplianceProjectNotFoundException(
                project_id
            )

        documents, total = (
            await self.document_repository.list_by_project(
                project_id=project.id,
                pagination=pagination,
            )
        )

        return PaginatedResponse[
            ComplianceDocumentResponse
        ](
            items=[
                ComplianceDocumentResponse.model_validate(
                    document
                )
                for document in documents
            ],
            total=total,
            offset=pagination.offset,
            limit=pagination.limit,
        )

    async def get_document_download_url(
        self,
        *,
        project_id: UUID,
        document_id: UUID,
        current_user: User,
    ) -> str:
        organization_id = get_user_organization_id(
            current_user
        )

        project = (
            await self.project_repository
            .get_by_id_and_organization(
                project_id=project_id,
                organization_id=organization_id,
            )
        )

        if project is None:
            raise ComplianceProjectNotFoundException(
                project_id
            )

        document = (
            await self.document_repository
            .get_by_id_and_project(
                document_id=document_id,
                project_id=project.id,
            )
        )

        if document is None:
            raise ComplianceDocumentNotFoundException(
                document_id
            )

        return (
            await self.storage_service
            .generate_download_url(
                document.storage_key
            )
        )