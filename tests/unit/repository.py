from sqlalchemy.ext.asyncio import AsyncSession
from tik_tok.models.users import User


class TestUserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, username: str, email: str, password: str) -> User:
        user = User(username=username, email=email, hashed_password=password)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_user(self, user_id: int) -> User:
        return await self.session.get(User, user_id)

    async def update_user(self, user_id: int, **kwargs) -> User:
        user = await self.session.get(User, user_id)
        for key, value in kwargs.items():
            setattr(user, key, value)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete_user(self, user_id: int):
        user = await self.session.get(User, user_id)
        await self.session.delete(user)
        await self.session.commit()
