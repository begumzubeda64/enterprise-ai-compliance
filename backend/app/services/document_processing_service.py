import hashlib
from pathlib import Path

from fastapi import UploadFile

from app.exceptions.compliance_document import (
    DocumentTooLargeException,
    EmptyDocumentException,
    UnsupportedDocumentTypeException,
)


class DocumentProcessingService:
    """
    Handles validation and metadata extraction for uploaded documents.
    """

    SUPPORTED_EXTENSIONS = {
        ".pdf",
        ".docx",
        ".txt",
    }

    MAX_FILE_SIZE_MB = 20
    MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

    def validate_file_type(
        self,
        file: UploadFile,
    ) -> str:
        """
        Validate the file extension and return it in lowercase.
        """

        extension = Path(
            file.filename or ""
        ).suffix.lower()

        if extension not in self.SUPPORTED_EXTENSIONS:
            raise UnsupportedDocumentTypeException()

        return extension

    async def get_file_size(
        self,
        file: UploadFile,
    ) -> int:
        """
        Return the file size and restore the file pointer.
        """

        await file.seek(0)

        size = 0

        while chunk := await file.read(1024 * 1024):
            size += len(chunk)

            if size > self.MAX_FILE_SIZE_BYTES:
                await file.seek(0)

                raise DocumentTooLargeException(
                    self.MAX_FILE_SIZE_MB
                )

        await file.seek(0)

        if size == 0:
            raise EmptyDocumentException()

        return size

    async def calculate_sha256(
        self,
        file: UploadFile,
    ) -> str:
        """
        Calculate SHA-256 and restore the file pointer.
        """

        hasher = hashlib.sha256()

        await file.seek(0)

        while chunk := await file.read(1024 * 1024):
            hasher.update(chunk)

        await file.seek(0)

        return hasher.hexdigest()