from contextlib import asynccontextmanager
import aioboto3
from fastapi import UploadFile
from tik_tok.core.config import settings

class S3Client:
    def __init__(self, bucket_name: str):
        self.bucket_name = bucket_name
        self.config = {
            "aws_access_key_id": settings.s3_access_key,
            "aws_secret_access_key": settings.s3_secret_key,
            "endpoint_url": settings.s3_endpoint,
        }

    @asynccontextmanager
    async def client(self):
        session = aioboto3.Session()
        async with session.client("s3", **self.config) as client:
            yield client

    async def test_connection(self):
        try:
            async with self.client() as client:
                await client.list_buckets()
        except Exception as e:
            raise RuntimeError(f"Failed to connect to S3: {e}")

    async def upload_file(self, file: UploadFile, key: str) -> None:
        try:
            async with self.client() as client:
                await client.put_object(
                    Bucket=self.bucket_name,
                    Key=key,
                    Body=await file.read(),
                )
        except Exception as e:
            raise RuntimeError(f"Failed to upload file: {e}")

    async def delete_file(self, key: str) -> None:
        try:
            async with self.client() as client:
                await client.delete_object(Bucket=self.bucket_name, Key=key)
        except Exception as e:
            raise RuntimeError(f"Failed to delete file: {e}")

    async def download_file(self, key: str) -> bytes:
        try:
            async with self.client() as client:
                response = await client.get_object(Bucket=self.bucket_name, Key=key)
                return await response["Body"].read()
        except Exception as e:
            raise RuntimeError(f"Failed to download file: {e}")

    async def list_files(self, prefix: str = "") -> list:
        try:
            async with self.client() as client:
                response = await client.list_objects_v2(Bucket=self.bucket_name, Prefix=prefix)
                return [obj["Key"] for obj in response.get("Contents", [])]
        except Exception as e:
            raise RuntimeError(f"Failed to list files: {e}")