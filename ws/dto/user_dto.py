import uuid
from ws.dto.base import BaseDTO


class UserDTO(BaseDTO):
    uuididf: uuid.UUID
    username: str
    password: str
    role_uuididf: uuid.UUID
