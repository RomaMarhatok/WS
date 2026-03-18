from random import choice
from ws.test.fixtures.factories import BaseFactory, fake
from ws.db.models import Users, Roles


class UserFactory(BaseFactory):
    def __init__(self, session_factory):
        super().__init__(session_factory)

    @property
    def model(self):
        return Users

    async def get_instances(self):
        return [
            self.model(
                username=fake.user_name(),
                password=fake.password(length=8),
                role_id=choice(await self.get_model_ids(Roles)),
            )
            for _ in range(5)
        ]
