from ws.api.v1.schemas.role import RoleNameEnum
from ws.db.models import Roles
from ws.test.fixtures.factories import BaseFactory


class RoleFactory(BaseFactory):

    def __init__(self, session_factory):
        super().__init__(session_factory)
        self.rolenames = RoleNameEnum.get_all_roles()

    @property
    def model(self):
        return Roles

    async def create(self):
        roles = [self.model(rolename=rolename) for rolename in self.rolenames]
        role_ids = await self.save_instances(roles)
        self.models_cache_ids.update({self.model.__tablename__: role_ids})
