from typing import List
from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from schemas.user import UserRead
from models import database_manager
from crud.users import get_all_users

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("", response_model=List[UserRead])
async def get_users(
    session: AsyncSession = Depends(database_manager.session_getter)
):
    users = await get_all_users(session=session)
    print(users)
    return users