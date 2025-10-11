from ws.dto.role import RoleNameEnum
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
        uuididfs = self.generate_uuid_collection(
            self.model.__tablename__, len(self.rolenames)
        )
        roles = [
            self.model(uuididf=uuididf, rolename=rolename)
            for rolename, uuididf in zip(self.rolenames, uuididfs)
        ]
        await self.save_instances(roles)
