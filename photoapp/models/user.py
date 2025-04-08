from typing import List, TYPE_CHECKING
from datetime import datetime

from sqlalchemy.orm import (
    Mapped, 
    mapped_column,
    relationship    
)
from sqlalchemy import DateTime, BigInteger, UniqueConstraint
from sqlalchemy.sql.expression import func

from models.base import ModelBase
from models.mixins.id_int_pk import IdIntPKMixin


if TYPE_CHECKING:
    from models.post import Post


class User(IdIntPKMixin, ModelBase):
    __table_args__ = (
        UniqueConstraint("sso_id", "sso_provider"),
    )

    sso_id: Mapped[int] = mapped_column(BigInteger)
    sso_provider: Mapped[str] = mapped_column()
    username: Mapped[str] = mapped_column()
    avatar_url: Mapped[str] = mapped_column()


    

    # TODO:
    # time_created: Mapped[datetime] = mapped_column(
    #     DateTime(timezone=True), 
    #     server_default=func.now()
    # )
    # time_updated: Mapped[datetime] = mapped_column(
    #     DateTime(timezone=True), 
    #     onupdate=func.now()
    # )
    # TODO: add provider
    
    posts: Mapped[List["Post"]] = relationship(back_populates="user")