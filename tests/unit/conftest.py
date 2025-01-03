import pytest
import pytest_asyncio
from httpx import AsyncClient
from asgi_lifespan import LifespanManager
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import delete

from tik_tok.core.s3_client import S3Client
from tik_tok.main import app
from tik_tok.models.base import Base
from tik_tok.models.users import User
from tik_tok.core.database import get_async_session
from tik_tok.tasks.video_tasks import s3_bucket_service_factory

TEST_DATABASE_URL = "sqlite+aiosqlite:///test_db.sqlite"


@pytest.fixture
async def setup_s3():
    for test_file in TEST_DATABASE_URL:
        await S3Client.upload_file(test_file, f"uploads/{test_file}")
    yield
    # Удаляем тестовые файлы
    for test_file in TEST_DATABASE_URL:
        await S3Client.delete_file(f"uploads/{test_file}")


@pytest.fixture
def test_video_file():
    return "test_video.mp4"


@pytest_asyncio.fixture
async def test_db():
    """Инициализация тестовой базы данных."""
    engine = create_async_engine(TEST_DATABASE_URL, echo=True)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield async_session
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture
async def override_get_async_session(test_db):
    """Переопределение зависимости базы данных."""

    async def _get_test_session():
        async with test_db() as session:
            yield session

    app.dependency_overrides[get_async_session] = _get_test_session
    yield
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def test_client(override_get_async_session):
    """Клиент для тестирования."""
    async with LifespanManager(app):
        async with AsyncClient(base_url="http://testserver") as client:
            yield client


@pytest_asyncio.fixture
async def setup_db(test_db):
    """Очистка базы данных перед каждым тестом."""
    async with test_db() as session:
        await session.execute(delete(User))
        await session.commit()
    yield


@pytest.fixture(scope="session", autouse=True)
def setup_minio():
    # Подключение к MinIO
    s3_service = s3_bucket_service_factory(".env")
    s3_service.create_s3_client()
