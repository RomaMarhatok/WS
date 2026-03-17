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
        users = [
            self.model(
                username=fake.user_name(),
                password=fake.password(length=8),
                role_uuididf=choice(self.get_model_cached_ids(Roles.__tablename__)),
            )
            for _ in range(5)
        ]
        user_ids = await self.save_instances(users)
        self.models_cache_ids.update({self.model.__name__: user_ids})
