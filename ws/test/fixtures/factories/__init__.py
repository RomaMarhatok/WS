from typing import Sequence, Generic
from random import randint

from faker import Faker

from sqlalchemy import select

from ws.db.session import SessionManager
from ws.db.repository.generic_repository import SQLALCHEMY_MODEL_TYPE


fake = Faker()


class BaseFactory(Generic[SQLALCHEMY_MODEL_TYPE]):

    def __init__(self, db: SessionManager):
        self.db = db

    @property
    def model(self) -> SQLALCHEMY_MODEL_TYPE:
        raise NotImplementedError

    async def get_instances(self) -> Sequence[SQLALCHEMY_MODEL_TYPE]:
        raise NotImplementedError

    async def create(self):
        async with self.db.get_db_session() as session:
            instances = await self.get_instances()
            session.add_all(instances)
            await session.commit()

    async def is_exist(self):
        async with self.db.get_db_session() as session:
            result = await session.execute(select(self.model))
            return len(result.scalars().all()) > 0

    def _get_random_number(self, min: int, max: int) -> int:
        return randint(min, max)

    async def get_model_ids(self, model: SQLALCHEMY_MODEL_TYPE) -> Sequence[int]:
        async with self.db.get_db_session() as session:
            result = await session.execute(select(model.id))
            return result.scalars().all()
