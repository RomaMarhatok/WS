import uuid
from ws.dto.base import BaseDBModelDTO


class UserDTO(BaseDBModelDTO):
    uuididf: uuid.UUID
    username: str
    password: str
    role_uuididf: uuid.UUID
