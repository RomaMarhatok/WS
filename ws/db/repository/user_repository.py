import uuid
from ws.db.models import Users
from ws.db.dto import UserDTO
from ws.db.repository.base_repository import GenericRepository


class UserRepository(GenericRepository[Users, UserDTO]):
    @property
    def _model(self):
        return Users

    async def save(
        self,
        dto: UserDTO,
    ) -> Users:
        async with self.session_factory() as session:
            user = self._model(**dto)
            session.add(user)
            await session.commit()
            return user

    async def get_by_uuididf(self, uuididf: uuid):
        async with self.session_factory() as session:
            user = await session.get(Users, uuididf=uuididf)
            return user

    async def update(self, new_dto: UserDTO):
        async with self.session_factory() as session:
            user = self._model(**new_dto)
            merged_user = await session.merge(user)
            await session.commit()
            return merged_user

    async def delete(self, uuididf: uuid) -> bool:
        async with self.session_factory() as session:
            user = await session.get(self._model, uuididf=uuididf)
            await session.delete(user)
            await session.commit()
