from ws.api.v1.schemas.role import RoleNameEnum
from ws.db.models import Roles
from ws.test.fixtures.factories import BaseFactory


class RoleFactory(BaseFactory):

    def __init__(self, session_factory):
        super().__init__(session_factory)

    @property
    def model(self):
        return Roles

    async def get_instances(self):
        rolenames = RoleNameEnum.get_all_roles()
        return [self.model(rolename=rolename) for rolename in rolenames]
