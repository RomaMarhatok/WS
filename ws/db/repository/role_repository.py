from ws.api.v1.schemas.role import RoleDTO
from ws.db.models import Roles
from .generic_repository import GenericRepository


class RoleRepository(GenericRepository[Roles, RoleDTO, RoleDTO]):
    pass
