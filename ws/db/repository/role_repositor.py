from ws.db.repository.base_repository import GenericRepository
from ws.db.models import Roles
from ws.dto import RoleDTO


class RoleRepository(GenericRepository[Roles, RoleDTO]):

    @property
    def _model(self):
        return Roles
