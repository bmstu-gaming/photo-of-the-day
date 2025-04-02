from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import User

# TODO: add pagination (offset + limit)
async def get_all_users(session: AsyncSession) -> Sequence[User]:
    """
    SELECT id, username from users
    ORDER BY id;
    """
    statement = select(User.id, User.username).order_by(User.id)
    result = await session.execute(statement)
    return result.all()

