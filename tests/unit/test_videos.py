import pytest
from aioboto3.s3.inject import upload_file
from fastapi.testclient import TestClient
from httpx import AsyncClient
from tik_tok.core.config import settings
from tik_tok.core.database import get_async_session
from tik_tok.core.s3_client import S3Client
from tik_tok.main import app
from tik_tok.models.videos import Video
from tik_tok.tasks.video_processing import s3_bucket_service_factory


@pytest.mark.asyncio
async def test_upload_video(test_video_file):
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Загружаем файл
        with open(test_video_file, "rb") as file:
            response = await client.post("/upload", files={"file": file})
        assert response.status_code == 200
        assert response.json() == {"message": "Видео загружено успешно"}

        # Проверка загрузки файла в S3
        assert await upload_file(
            settings.s3_bucket_name, test_video_file, test_video_file
        )

        # Проверка сохранения метаданных в базе
        async with get_async_session() as session:
            video = await session.query(Video).filter_by(title=test_video_file).first()
            assert video is not None
            assert (
                video.file_url
                == f"{settings.s3_endpoint}/{settings.s3_bucket_name}/{test_video_file}"
            )

        # Удаление тестового файла из S3
        assert await delete_file_from_s3(settings.s3_bucket_name, test_video_file)


@pytest.mark.asyncio
async def test_list_files(setup_s3):
    files = await S3Client.list_files("uploads")
    assert len(files) == len(TEST_FILES)


@pytest.mark.asyncio
async def test_delete_file(setup_s3):
    await s3_service.delete_file("uploads/test1.mp4")
    files = await s3_service.list_files("uploads")
    assert "uploads/test1.mp4" not in files
