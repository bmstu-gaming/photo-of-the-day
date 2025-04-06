from typing import Annotated

from fastapi import Depends
from fastapi.templating import Jinja2Templates

from sqlalchemy.ext.asyncio import AsyncSession

from database import database_manager


templates = Jinja2Templates(directory="templates")

session_dependency = Annotated[AsyncSession, Depends(database_manager.session_getter)]

# TODO: auth dependency