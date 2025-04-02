from typing import TYPE_CHECKING

from sqlalchemy.orm import (
    Mapped, 
    mapped_column, 
    relationship
)
from sqlalchemy import ForeignKey

from .base import ModelBase

# Circular impoer fix - this will act as imported only on code editing
# not runtime
if TYPE_CHECKING:
    from .user import User

class Post(ModelBase):
    user_id: Mapped[int] = mapped_column(ForeignKey(f"users.id"))
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    image_path: Mapped[str] = mapped_column()

    # when using annotations we need to declare the type imported from file
    user: Mapped["User"] = relationship(back_populates="posts")

