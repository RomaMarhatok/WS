import uuid
from ws.dto.base import BaseDTO


class UserDTO(BaseDTO):
    username: str
    password: str
    role_uuididf: uuid.UUID
