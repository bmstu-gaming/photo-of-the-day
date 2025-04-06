from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy.orm import (
    Mapped, 
    mapped_column, 
    relationship
)
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from sqlalchemy.sql.expression import func

from models.base import ModelBase
from models.mixins.id_int_pk import IdIntPKMixin

# Circular import fix - this will act as imported only on code editing
# not runtime (required by user dependency)
if TYPE_CHECKING:
    from models.user import User


class Post(IdIntPKMixin, ModelBase):
    user_id: Mapped[int] = mapped_column(ForeignKey(f"users.id"))
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    image_path: Mapped[str] = mapped_column()
    
    # TODO:
    # date_created: Mapped[datetime] = mapped_column(
    #     DateTime(timezone=True),
    #     server_default=func.utcnow()
    # )

    user: Mapped["User"] = relationship(back_populates="posts")

