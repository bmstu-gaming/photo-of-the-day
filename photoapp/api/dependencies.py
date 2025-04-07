from typing import Annotated

from fastapi import Depends, Request
from fastapi.templating import Jinja2Templates

from sqlalchemy.ext.asyncio import AsyncSession

from database import database_manager


# TODO: move to oauth.py?
# TODO: do i need to ask for user info again?
async def get_current_user(request: Request):
    user = request.session.get("user")
    if not user:
        return None
    return user


templates = Jinja2Templates(directory="templates")
session_dependency = Annotated[AsyncSession, Depends(database_manager.session_getter)]
user_dependency = Annotated[dict, Depends(get_current_user)]


