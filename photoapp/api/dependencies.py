from typing import Annotated

from fastapi import Depends, Request
from fastapi.templating import Jinja2Templates

from sqlalchemy.ext.asyncio import AsyncSession

from database import database_manager
import crud.users as crud_users

from schemas.user import UserRead


templates = Jinja2Templates(directory="templates")
session_dependency = Annotated[AsyncSession, Depends(database_manager.session_getter)]


# Here we read user id from session and if it exists, we return user data from DB
async def get_current_user(
    request: Request,
    session: session_dependency
) -> UserRead:
    user = request.session.get("user")
    if not user:
        return None
    db_user = await crud_users.get_sso_user(
        session=session, 
        user_sso_id=user['id'], 
        user_sso_provider=user['provider']
    )
    return db_user


user_dependency = Annotated[dict, Depends(get_current_user)]
