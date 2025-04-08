from typing import List
from fastapi import APIRouter

from schemas.post import PostRead, PostCreate

import crud.posts as crud_posts

from .dependencies import session_dependency


router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)


@router.get("", response_model=List[PostRead])
async def get_posts(
    session: session_dependency
):
    posts = await crud_posts.get_all_posts(session=session)
    return posts


# @router.post("", response_model=PostRead)
# async def create_post(
#     session: session_dependency,
#     post_create: PostCreate
# ):
#     post = await crud_posts.create_post(session=session, post_schema=post_create)
#     return post