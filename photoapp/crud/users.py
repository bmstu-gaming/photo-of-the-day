from typing import Sequence

from fastapi import HTTPException, status

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import User
from schemas.user import UserCreate


# TODO: add pagination (offset + limit)
async def get_all_users(session: AsyncSession) -> Sequence[User]:
    """
    SELECT id, username from users
    ORDER BY id;
    """
    statement = select(User.id, User.username).order_by(User.id)
    result = await session.execute(statement)
    return result.all()


async def get_user_by_id(
    session: AsyncSession,
    user_id: int
) -> User | None:
    """
    SELECT id, username from users
    WHERE id = :user_id;
    """
    statement = select(User.id, User.username).where(User.sso_id == user_id)
    user = await session.execute(statement)
    user = user.first()
    if not user:
        return None
    return user


async def create_user(
    session: AsyncSession,
    user_schema: UserCreate
) -> User:
    # load to User (user_schema validates everything)
    new_user = User(**user_schema.model_dump())
    session.add(new_user)
    await session.commit()

    # refresh data when creating
    await session.refresh(new_user)
    return new_user
