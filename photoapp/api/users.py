from typing import List
from fastapi import APIRouter, HTTPException, status

from schemas.user import UserRead, UserCreate, UserUpdate

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
    """
    Get all users
    """
    users = await crud_users.get_all_users(session=session)
    return users


@router.get("/{user_sso_provider}/{user_sso_id}", response_model=UserRead)
async def get_sso_user(
    session: session_dependency,
    user_sso_id: int,
    user_sso_provider: str
):
    """
    Get user by SSO ID and provider
    """
    user = await crud_users.get_sso_user(
        session=session, 
        user_sso_id=user_sso_id,
        user_sso_provider=user_sso_provider,
    )
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.post("", response_model=UserRead)
async def create_user(
    session: session_dependency,
    user_create: UserCreate,
):
    """
    Create user
    """
    user = await crud_users.create_user(session=session, user_schema=user_create)
    return user


@router.put("/{user_sso_provider}/{user_sso_id}", response_model=UserRead)
async def update_user(
    session: session_dependency,
    user_sso_id: int,
    user_sso_provider: str,
    user_update: UserUpdate,
):
    """
    Update user
    """
    updated_user = await crud_users.update_sso_user(
        session=session,
        user_sso_id=user_sso_id,
        user_sso_provider=user_sso_provider, 
        user_schema=user_update)
    return updated_user