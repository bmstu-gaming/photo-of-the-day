from typing import List, Annotated
from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from schemas.user import UserRead, UserCreate
from models import database_manager

import crud.users as crud_users
# from crud.users import get_all_users, create_user


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("", response_model=List[UserRead])
async def get_users(
    # session: AsyncSession = Depends(database_manager.session_getter)
    # Better way:
    session: Annotated[AsyncSession, Depends(database_manager.session_getter)]
):
    users = await crud_users.get_all_users(session=session)
    return users


@router.post("", response_model=UserRead)
async def create_user(
    session: Annotated[AsyncSession, Depends(database_manager.session_getter)],
    user_create: UserCreate,
):
    user = await crud_users.create_user(session=session, user_schema=user_create)
    return user