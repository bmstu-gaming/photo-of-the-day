from datetime import datetime

from pydantic import (
    BaseModel, ConfigDict
)


class PostBase(BaseModel):
    user_id: int
    title: str
    description: str
    image_path: str
    date_created: datetime


class PostCreate(PostBase):
    pass


class PostRead(BaseModel):
    id: int
    title: str
    description: str
    image_path: str
    username: str

    model_config = ConfigDict(
        from_attributes=True,
    )
