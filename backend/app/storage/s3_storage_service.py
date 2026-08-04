import asyncio
from typing import BinaryIO
from uuid import UUID

import boto3
from botocore.client import BaseClient

from app.core.config import settings
from app.storage.base import BaseStorageService


class S3StorageService(BaseStorageService):
    """
    Amazon S3 implementation of the storage interface.
    """

    def __init__(self) -> None:
        self.bucket_name = settings.aws_s3_bucket_name

        self.client: BaseClient = boto3.client(
            "s3",
            region_name=settings.aws_region,
        )

    async def verify_bucket_access(self) -> None:
        await asyncio.to_thread(
            self.client.head_bucket,
            Bucket=self.bucket_name,
        )

    def generate_stored_filename(
        self,
        *,
        document_id: UUID,
        extension: str,
    ) -> str:
        return f"{document_id}{extension}"

    def build_document_storage_key(
        self,
        *,
        organization_id: UUID,
        project_id: UUID,
        document_id: UUID,
        stored_filename: str,
    ) -> str:
        return (
            f"organizations/{organization_id}/"
            f"projects/{project_id}/"
            f"documents/{document_id}/"
            f"{stored_filename}"
        )

    async def upload_file(
        self,
        *,
        file: BinaryIO,
        object_key: str,
        content_type: str,
        metadata: dict[str, str] | None = None,
    ) -> None:
        extra_args: dict[str, object] = {
            "ContentType": content_type,
        }

        if metadata:
            extra_args["Metadata"] = metadata

        await asyncio.to_thread(
            self.client.upload_fileobj,
            file,
            self.bucket_name,
            object_key,
            ExtraArgs=extra_args,
        )

    async def delete_file(
        self,
        object_key: str,
    ) -> None:
        await asyncio.to_thread(
            self.client.delete_object,
            Bucket=self.bucket_name,
            Key=object_key,
        )

    async def generate_download_url(
        self,
        object_key: str,
        expires_in_seconds: int = 900,
    ) -> str:
        return await asyncio.to_thread(
            self.client.generate_presigned_url,
            "get_object",
            Params={
                "Bucket": self.bucket_name,
                "Key": object_key,
            },
            ExpiresIn=expires_in_seconds,
        )