from random import choice
from ws.test.fixtures.factories import BaseFactory, fake
from ws.db.models import Users, Roles


class UserFactory(BaseFactory):
    def __init__(self, session_factory):
        super().__init__(session_factory)

    @property
    def model(self):
        return Users

    async def create(self):
        uuididfs = self.generate_uuid_collection(self.model.__tablename__, 5)
        users = [
            self.model(
                uuididf=uuididf,
                username=fake.user_name(),
                password=fake.password(length=8),
                role_uuididf=choice(
                    list(self.get_collection().get(Roles.__tablename__))
                ),
            )
            for uuididf in uuididfs
        ]
        await self.save_instances(users)
