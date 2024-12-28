import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.unit.repository import TestUserRepository


@pytest.mark.asyncio
async def test_create_user(test_db: AsyncSession):
    """Тест создания пользователя."""
    async with test_db() as session:
        repo = TestUserRepository(session)
        user = await repo.create_user("test_user", "test@example.com", "securepassword")
        assert user.username == "test_user"
        assert user.email == "test@example.com"


@pytest.mark.asyncio
async def test_get_user(test_db):
    """Тест получения пользователя по ID."""
    async with test_db() as session:
        repo = TestUserRepository(session)
        user = await repo.create_user("test_user", "test@example.com", "securepassword")
        retrieved_user = await repo.get_user(user.id)
        assert retrieved_user.username == "test_user"


@pytest.mark.asyncio
async def test_update_user(test_db):
    """Тест обновления данных пользователя."""
    async with test_db() as session:
        repo = TestUserRepository(session)
        user = await repo.create_user("test_user", "test@example.com", "securepassword")
        updated_user = await repo.update_user(user.id, username="updated_user")
        assert updated_user.username == "updated_user"


@pytest.mark.asyncio
async def test_delete_user(test_db: AsyncSession):
    """Тест удаления пользователя."""
    async with test_db() as session:
        repo = TestUserRepository(session)
        user = await repo.create_user("test_user", "test@example.com", "securepassword")
        await repo.delete_user(user.id)
        deleted_user = await repo.get_user(user.id)
        assert deleted_user is None


#
# @pytest.mark.asyncio
# async def test_register_user_parametrize(test_client: AsyncClient, setup_db):
#     """Тест регистрации пользователя."""
#     payload = {
#         "username": "new_user",
#         "email": "new@example.com",
#         "password": "securepassword",
#     }
#     response = await test_client.post("/users/register", json=payload)
#     assert response.status_code == 201
#     assert response.json()["username"] == "new_user"
