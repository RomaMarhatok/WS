from uuid import UUID
from abc import ABC
from ws.enums.types import SchemasTypes
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncSession,
)


class BaseRepository(ABC):

    @property
    def _model(self):
        raise NotImplementedError

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self.session_factory = session_factory

    async def save(self, creation_data: SchemasTypes.PYDANTIC_SCHEMA_TYPE.value):
        "The save method is used to create a record without returning the saved instance"
        raise NotImplementedError

    async def create(
        self, creation_data: SchemasTypes.PYDANTIC_SCHEMA_TYPE.value
    ) -> SchemasTypes.SQLALCHEMY_MODEL_TYPE.value:
        "The create method is used to create a record with returning the saved instance"
        raise NotImplementedError

    async def get(
        self, filters: SchemasTypes.PYDANTIC_SCHEMA_TYPE.value
    ) -> SchemasTypes.SQLALCHEMY_MODEL_TYPE.value:
        "The get method is used to create a record with returning the saved instance"
        raise NotImplementedError

    async def update(
        self, uuididf: UUID, update_data: SchemasTypes.PYDANTIC_SCHEMA_TYPE.value
    ) -> SchemasTypes.SQLALCHEMY_MODEL_TYPE.value:
        """Update instance by uuid"""
        raise NotImplementedError

    async def delete(self, uuididf: UUID) -> UUID:
        "The delete method is deleted instance by uuididf"

        raise NotImplementedError
