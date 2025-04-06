from typing import List, TYPE_CHECKING

from sqlalchemy.orm import (
    Mapped, 
    mapped_column,
    relationship    
)

from models.base import ModelBase
from models.mixins.id_int_pk import IdIntPKMixin

posts_tablename = ''

if TYPE_CHECKING:
    from models.post import Post


class User(IdIntPKMixin, ModelBase):
    username: Mapped[str] = mapped_column(unique=True)
    posts: Mapped[List["Post"]] = relationship(back_populates="user")