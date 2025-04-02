# from sqlalchemy import UniqueConstraint
from typing import List, TYPE_CHECKING

from sqlalchemy.orm import (
    Mapped, 
    mapped_column,
    relationship    
)

from .base import ModelBase
from .mixins.id_int_pk import IdIntPKMixin

posts_tablename = ''

if TYPE_CHECKING:
    from .post import Post


class User(IdIntPKMixin, ModelBase):
    username: Mapped[str] = mapped_column(unique=True)

    posts: Mapped[List["Post"]] = relationship(back_populates="user")