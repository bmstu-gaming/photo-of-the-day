from typing import List
from fastapi import APIRouter

from schemas.user import UserRead, UserCreate

import crud.users as crud_users

from api.dependencies import session_dependency

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("", response_model=List[UserRead])
async def get_users(
    # session: AsyncSession = Depends(database_manager.session_getter)
    # Better way:
    session: session_dependency
):
    users = await crud_users.get_all_users(session=session)
    return users


@router.post("", response_model=UserRead)
async def create_user(
    session: session_dependency,
    user_create: UserCreate,
):
    user = await crud_users.create_user(session=session, user_schema=user_create)
    return user