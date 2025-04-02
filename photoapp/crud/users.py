from typing import Sequence

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
