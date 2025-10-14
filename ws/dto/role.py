from enum import Enum
from ws.dto.base import BaseDBModelDTO


class RoleNameEnum(Enum):
    BASE_USER = "base_user"
    ADMIN = "admin"

    @classmethod
    def get_all_roles(cls) -> list[str]:
        return [member.value for member in cls]


class RoleDTO(BaseDBModelDTO):
    rolename: str
