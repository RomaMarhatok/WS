import uuid
from pydantic import BaseModel


class UserDTO(BaseModel):
    uuididf: uuid
    username: str
    password: str
    role_uuididf: uuid
