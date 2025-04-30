from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Post
from models import User

# TODO: add pagination (offset + limit)
# TODO: add timestamp
async def get_all_posts(session: AsyncSession) -> Sequence[Post]:
    """
    select p.id, p.title, p.description, p.image_path, u.username
    from users as u 
        join posts as p
        on p.user_id = u.id
    order by p.id;
    """
    statement = select(
        Post.id, Post.title, Post.description, Post.image_path, User.username
    ).join(User, Post.user_id == User.id
    ).order_by(Post.id)
    
    result = await session.execute(statement)
    return result.all()


async def create_post(session: AsyncSession) -> Post:
    """
    INSERT INTO public.posts
    (user_id, title, description, image_path)
    values
        (1, 'post_title', 'post_description', 'path');
    """
    pass


# async def update_post(session: AsyncSession) -> Post:
#     pass

# async def delete_post(session: AsyncSession)