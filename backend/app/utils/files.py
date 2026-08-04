import hashlib
import os
import uuid
from pathlib import Path

from fastapi import UploadFile

from app.exceptions.compliance_document import (
    UnsupportedDocumentTypeException,
)


_SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt",
}


def get_file_extension(
    filename: str,
) -> str:
    """
    Return the lowercase file extension.
    """

    return Path(filename).suffix.lower()


def validate_file_extension(
    filename: str,
) -> None:
    """
    Validate that the uploaded file type is supported.
    """

    extension = get_file_extension(
        filename,
    )

    if extension not in _SUPPORTED_EXTENSIONS:
        raise UnsupportedDocumentTypeException()


async def calculate_sha256(
    file: UploadFile,
) -> str:
    """
    Calculate the SHA-256 checksum of an uploaded file.

    The file pointer is restored afterwards.
    """

    hasher = hashlib.sha256()

    await file.seek(0)

    while chunk := await file.read(1024 * 1024):
        hasher.update(chunk)

    await file.seek(0)

    return hasher.hexdigest()


def generate_stored_filename(
    original_filename: str,
) -> str:
    """
    Generate a unique filename while preserving
    the original extension.
    """

    extension = get_file_extension(
        original_filename,
    )

    return f"{uuid.uuid4()}{extension}"


def build_storage_key(
    *,
    organization_id: uuid.UUID,
    project_id: uuid.UUID,
    stored_filename: str,
) -> str:
    """
    Build the S3 object key.
    """

    return (
        "organizations/"
        f"{organization_id}/"
        f"projects/{project_id}/"
        f"{stored_filename}"
    )


async def get_file_size(
    file: UploadFile,
) -> int:
    """
    Return the uploaded file size in bytes.
    """

    await file.seek(0, os.SEEK_END)

    size = file.file.tell()

    await file.seek(0)

    return size