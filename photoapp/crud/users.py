from typing import Sequence

from sqlalchemy import select, and_, update
from sqlalchemy.ext.asyncio import AsyncSession

from models import User
from schemas.user import UserCreate, UserUpdate


# TODO: add pagination (offset + limit)
async def get_all_users(session: AsyncSession) -> Sequence[User]:
    """
    SELECT id, sso_id, username, vatar_url from users
    ORDER BY id;
    """
    statement = select(
        User.id, User.sso_id, User.username, User.avatar_url, User.sso_provider
    ).order_by(User.id)

    result = await session.execute(statement)
    return result.all()


async def get_sso_user(
    session: AsyncSession,
    user_sso_id: int,
    user_sso_provider: str,
) -> User | None:
    """
    SELECT id, username from users
    WHERE sso_id = :user_sso_id AND sso_provider = :user_sso_provider;
    """
    statement = select(
        User.id, User.sso_id, User.username, User.avatar_url, User.sso_provider
    ).where(and_(
        User.sso_id == user_sso_id, 
        User.sso_provider == user_sso_provider)
    )

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
    try:
        session.add(new_user)
        await session.commit()
        # refresh data when creating
        await session.refresh(new_user)
        return new_user
    except:
        # In case anything breaks - rollback
        await session.rollback()
        raise


async def update_sso_user(
    session: AsyncSession,
    user_sso_id: int,
    user_sso_provider: str,
    user_schema: UserUpdate,
):   
    statement = update(User
        ).where(and_(
            User.sso_id == user_sso_id,
            User.sso_provider == user_sso_provider)
        ).values(user_schema.model_dump())
    
    await session.execute(statement)
    await session.commit()
    
    updated_user = await get_sso_user(
        session=session,
        user_sso_id=user_sso_id,
        user_sso_provider=user_sso_provider
    )
    return updated_user


async def create_user_if_not_exist(
    session: AsyncSession,
    user_schema: UserCreate
) -> User:
    
    db_user = await get_sso_user(
        session=session,
        user_sso_id=user_schema.sso_id,
        user_sso_provider=user_schema.sso_provider,
    )
    # If user exists - update user info
    if db_user:
        # Here it gets a bit tricky - we want to reduce our UserCreate mode to UserUpdate only
        # So only username and avatar url will be updated!
        # We assume that sso_id + provider combination does not change for users
        # if any of these change - we assume it is a new user 
        user_update = UserUpdate(**user_schema.model_dump(include=set(UserUpdate.model_fields)))

        updated_user = await update_sso_user(
            session=session,
            user_sso_id=user_schema.sso_id,
            user_sso_provider=user_schema.sso_provider,
            user_schema=user_update
        )
        return updated_user
    # If user does not exist - create new user
    new_user = await create_user(session=session, user_schema=user_schema)
    return new_user
