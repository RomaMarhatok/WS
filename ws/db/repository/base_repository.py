import uuid
from abc import ABC, abstractmethod
from typing import Generic
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from ws.db.types import SQLALCHEMY_MODEL_TYPE, PYDANTIC_SCHEMA_TYPE
from ws.db.session import get_session_factory


class GenericRepository(ABC, Generic[SQLALCHEMY_MODEL_TYPE, PYDANTIC_SCHEMA_TYPE]):

    def __init__(
        self, session_factory: async_sessionmaker[AsyncSession] = get_session_factory()
    ):
        self.session_factory = session_factory

    @property
    def _model(self) -> SQLALCHEMY_MODEL_TYPE:
        raise NotImplementedError

    @abstractmethod
    async def save(self, dto: PYDANTIC_SCHEMA_TYPE) -> SQLALCHEMY_MODEL_TYPE:
        raise NotImplementedError

    @abstractmethod
    async def get_by_uuididf(self, uuididf: uuid) -> SQLALCHEMY_MODEL_TYPE:
        raise NotImplementedError

    @abstractmethod
    async def update(
        self, old_instance: SQLALCHEMY_MODEL_TYPE, new_dto: PYDANTIC_SCHEMA_TYPE
    ):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, uuididf: uuid) -> bool:
        raise NotImplementedError
