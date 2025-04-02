from typing import List, Annotated
from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from schemas.post import PostRead
from models import database_manager

import crud.posts as crud_posts


router = APIRouter(
    prefix="/posts",
    tags=["Users"],
)


@router.get("", response_model=List[PostRead])
async def get_posts(
    session: Annotated[AsyncSession, Depends(database_manager.session_getter)]
):
    posts = await crud_posts.get_all_posts(session=session)
    return posts