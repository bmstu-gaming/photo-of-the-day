from pydantic import (
    BaseModel, ConfigDict
)


# All users come from external auth (SSO), so we keep sso_id and username
class UserBase(BaseModel):
    sso_id: int
    username: str
    avatar_url: str


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

    