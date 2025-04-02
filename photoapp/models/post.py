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

from .base import ModelBase

# Circular import fix - this will act as imported only on code editing
# not runtime
if TYPE_CHECKING:
    from .user import User

class Post(ModelBase):
    user_id: Mapped[int] = mapped_column(ForeignKey(f"users.id"))
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    image_path: Mapped[str] = mapped_column()
    
    # TODO:
    # date_created: Mapped[datetime] = mapped_column(
    #     DateTime(timezone=True),
    #     server_default=func.utcnow()
    # )

    # when using annotations we need to declare the type imported from file
    user: Mapped["User"] = relationship(back_populates="posts")

