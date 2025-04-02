# from sqlalchemy import UniqueConstraint
from typing import List, TYPE_CHECKING

from sqlalchemy.orm import (
    Mapped, 
    mapped_column,
    relationship    
)

from .base import ModelBase

posts_tablename = ''

if TYPE_CHECKING:
    from .post import Post


class User(ModelBase):
    username: Mapped[str] = mapped_column(unique=True)

    posts: Mapped[List["Post"]] = relationship(back_populates="user")