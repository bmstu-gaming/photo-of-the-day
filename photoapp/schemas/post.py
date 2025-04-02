from pydantic import (
    BaseModel, ConfigDict
)


class PostBase(BaseModel):
    user_id: int
    title: str
    description: str
    image_path: str


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
