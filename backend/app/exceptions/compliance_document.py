from uuid import UUID

from app.exceptions.base import (
    BadRequestException,
    ResourceNotFoundException,
)


class ComplianceDocumentNotFoundException(
    ResourceNotFoundException
):
    error_code = "COMPLIANCE_DOCUMENT_NOT_FOUND"

    def __init__(
        self,
        document_id: UUID,
    ):
        super().__init__(
            message=(
                f"Compliance document '{document_id}' "
                "was not found."
            )
        )


class UnsupportedDocumentTypeException(
    BadRequestException
):
    error_code = "UNSUPPORTED_DOCUMENT_TYPE"

    def __init__(self):
        super().__init__(
            message=(
                "Only PDF, DOCX, and TXT documents "
                "are supported."
            )
        )


class DocumentTooLargeException(
    BadRequestException
):
    error_code = "DOCUMENT_TOO_LARGE"

    def __init__(
        self,
        max_size_mb: int,
    ):
        super().__init__(
            message=(
                f"Document size cannot exceed "
                f"{max_size_mb} MB."
            )
        )


class EmptyDocumentException(
    BadRequestException
):
    error_code = "EMPTY_DOCUMENT"

    def __init__(self):
        super().__init__(
            message="Uploaded document is empty."
        )


class DocumentUploadFailedException(
    BadRequestException
):
    error_code = "DOCUMENT_UPLOAD_FAILED"

    def __init__(self):
        super().__init__(
            message="Failed to upload document."
        )