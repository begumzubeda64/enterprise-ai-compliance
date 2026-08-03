from functools import lru_cache

from app.storage.base import BaseStorageService
from app.storage.s3_storage_service import S3StorageService


@lru_cache
def get_storage_service() -> BaseStorageService:
    return S3StorageService()