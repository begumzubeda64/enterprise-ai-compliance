import asyncio
from typing import BinaryIO

import boto3
from botocore.client import BaseClient

from app.core.config import settings
from app.storage.base import BaseStorageService


class S3StorageService(BaseStorageService):
    """
    Storage adapter for private compliance documents in Amazon S3.
    """

    def __init__(self) -> None:
        self.bucket_name = settings.aws_s3_bucket_name

        self.client: BaseClient = boto3.client(
            "s3",
            region_name=settings.aws_region,
        )

    async def verify_bucket_access(self) -> None:
        """
        Verify that the configured bucket exists and is accessible.
        """

        await asyncio.to_thread(
            self.client.head_bucket,
            Bucket=self.bucket_name,
        )

    async def upload_file(
        self,
        *,
        file: BinaryIO,
        object_key: str,
        content_type: str,
        metadata: dict[str, str] | None = None,
    ) -> None:
        """
        Upload a binary file-like object to the configured S3 bucket.
        """

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
        """
        Delete an object from the configured S3 bucket.
        """

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
        """
        Generate a temporary presigned URL for downloading an object.
        """

        return await asyncio.to_thread(
            self.client.generate_presigned_url,
            "get_object",
            Params={
                "Bucket": self.bucket_name,
                "Key": object_key,
            },
            ExpiresIn=expires_in_seconds,
        )