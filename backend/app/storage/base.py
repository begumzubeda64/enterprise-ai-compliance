from abc import ABC, abstractmethod
from typing import BinaryIO
from uuid import UUID


class BaseStorageService(ABC):
    """
    Abstract interface for document storage providers.
    """

    @abstractmethod
    async def verify_bucket_access(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def generate_stored_filename(
        self,
        *,
        document_id: UUID,
        extension: str,
    ) -> str:
        raise NotImplementedError

    @abstractmethod
    def build_document_storage_key(
        self,
        *,
        organization_id: UUID,
        project_id: UUID,
        document_id: UUID,
        stored_filename: str,
    ) -> str:
        raise NotImplementedError

    @abstractmethod
    async def upload_file(
        self,
        *,
        file: BinaryIO,
        object_key: str,
        content_type: str,
        metadata: dict[str, str] | None = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_file(
        self,
        object_key: str,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def generate_download_url(
        self,
        object_key: str,
        expires_in_seconds: int = 900,
    ) -> str:
        raise NotImplementedError