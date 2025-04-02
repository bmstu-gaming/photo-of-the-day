from pydantic import BaseModel
from pydantic import ConfigDict


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    pass


class UserRead(UserBase):

    id: int
    # Reading from attrs to integrate with ORM models
    model_config = ConfigDict(
        from_attributes=True,
    )
    # Deprectated version
    # class Config:
    #    orm_mode = True
    # Now it is automatic - actually no need to declare

    