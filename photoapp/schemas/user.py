from pydantic import (
    BaseModel, ConfigDict
)


# These values can change
class UserUpdate(BaseModel):
    username: str
    avatar_url: str


# Identificators of SSO user
class UserBase(UserUpdate):
    sso_id: int
    sso_provider: str


# Same as UserBase, no additional fields
class UserCreate(UserBase):
    pass


# UserRead is the same as UserBase, but with id field
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

    