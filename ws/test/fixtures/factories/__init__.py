import uuid
from random import randint
from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from ws.db.models import BaseModel
from faker import Faker

fake = Faker()


class BaseFactory(ABC):

    uuididfs_collection: dict[str, set] = {}

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self.factory = session_factory

    async def save_instances(self, instances: list[BaseModel]):
        async with self.factory() as session:
            session.add_all(instances)
            await session.commit()

    @abstractmethod
    async def create(self):
        raise NotImplementedError

    @property
    def model(self):
        raise NotImplementedError

    def _get_random_number(self, min: int, max: int) -> int:
        return randint(min, max)

    def _get_list_of_uuidv4(self, length_of_list) -> list[str]:
        return set([uuid.uuid4() for _ in range(length_of_list)])

    def get_collection(self) -> dict[str, set]:
        return self.__class__.uuididfs_collection

    def _add_uuididfs_to_collection(self, tablename: str, collection: set):
        if tablename not in self.get_collection():
            self.get_collection()[tablename] = collection
        self.get_collection()[tablename].update(collection)

    def generate_uuid_collection(
        self, tablename: str, length_of_list: int
    ) -> list[uuid.UUID]:
        ids = self._get_list_of_uuidv4(length_of_list)
        self._add_uuididfs_to_collection(tablename, ids)
        return ids
