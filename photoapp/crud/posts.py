from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Post, User

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