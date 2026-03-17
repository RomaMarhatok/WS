from typing import Sequence
from random import randint
from abc import ABC, abstractmethod


from faker import Faker

from ws.db.session import SessionManager
from ws.db.models import BaseModel

fake = Faker()


class BaseFactory(ABC):

    models_cache_ids: dict[str, Sequence[int]] = {}

    def __init__(self, db: SessionManager):
        self.db = db

    async def save_instances(self, instances: list[BaseModel]) -> Sequence[int]:
        async with self.db.get_db_session() as session:
            session.add_all(instances)
            await session.flush()
            ids = [instance.id for instance in instances]
            await session.commit()
            return ids

    @abstractmethod
    async def create(self):
        raise NotImplementedError

    @property
    def model(self):
        raise NotImplementedError

    def _get_random_number(self, min: int, max: int) -> int:
        return randint(min, max)

    def get_model_cached_ids(self, model_name: str) -> dict[str, set]:
        return self.__class__.models_cache_ids.get(model_name, None)
