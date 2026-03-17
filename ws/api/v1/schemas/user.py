import uuid
from pydantic import BaseModel, Field


class _BaseUserModel(BaseModel):
    username: str = Field(min_length=4)
    password: str = Field(min_length=8)
    role_uuididf: uuid.UUID


class UserCreationDTO(_BaseUserModel):
    pass


class UserUpdateDTO(_BaseUserModel):
    pass


class UserGetDTO(BaseModel):
    username: str
    password: str
    role_uuididf: uuid.UUID = Field(default=None)
