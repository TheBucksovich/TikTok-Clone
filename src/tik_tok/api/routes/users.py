from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from tik_tok.core.database import get_async_session
from tik_tok.dto.users import UserResponseDTO, UserCreateDTO
from tik_tok.models.users import User
from tik_tok.services.auth import verify_password, create_access_token, hash_password

router = APIRouter()


@router.post("/register", response_model=UserResponseDTO)
async def register_user(
    user: UserCreateDTO,
    session: AsyncSession = Depends(get_async_session),
):
    result = await session.execute(select(User).where(User.email == user.email))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password),
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


@router.get("/login")
async def login_user(
    username: str,
    password: str,
    session: AsyncSession = Depends(get_async_session),
):
    result = await session.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/{user_id}", response_model=UserResponseDTO)
async def get_user(
    user_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserResponseDTO)
async def update_user(
    user_id: int,
    user_data: UserCreateDTO,
    session: AsyncSession = Depends(get_async_session),
):
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_query = (
        update(User)
        .where(User.id == user_id)
        .values(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hash_password(user_data.password),
        )
        .execution_options(synchronize_session="fetch")
    )
    await session.execute(update_query)
    await session.commit()

    result = await session.execute(select(User).where(User.id == user_id))
    updated_user = result.scalar_one_or_none()
    return updated_user


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await session.delete(user)
    await session.commit()

    return {"message": "User deleted"}
