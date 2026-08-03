from abc import ABC, abstractmethod
from typing import BinaryIO


class BaseStorageService(ABC):

    @abstractmethod
    async def verify_bucket_access(self) -> None:
        ...

    @abstractmethod
    async def upload_file(
        self,
        *,
        file: BinaryIO,
        object_key: str,
        content_type: str,
        metadata: dict[str, str] | None = None,
    ) -> None:
        ...

    @abstractmethod
    async def delete_file(
        self,
        object_key: str,
    ) -> None:
        ...

    @abstractmethod
    async def generate_download_url(
        self,
        object_key: str,
        expires_in_seconds: int = 900,
    ) -> str:
        ...