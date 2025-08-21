from sqlalchemy import select
from ws.db.exceptions import EntityNotFoundException
from ws.db.repository.base_repository import GenericRepository
from ws.db.models import Roles
from ws.dto import RoleDTO


class RoleRepository(GenericRepository[Roles, RoleDTO]):

    @property
    def _model(self):
        return Roles

    async def get_by_name(self, name: str) -> Roles:
        async with self.session_factory() as session:
            stmt = select(self._model).where(self._model.rolename == name)
            entity = (await session.execute(stmt)).scalar_one_or_none()
            if entity is None:
                raise EntityNotFoundException(
                    f"Entity {self._model.__name__} with name {name} not found"
                )
            return entity
