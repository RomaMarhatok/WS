from ws.db.types import SQLALCHEMY_MODEL_TYPE, PYDANTIC_SCHEMA_TYPE
from ws.db.repository.base_repository import GenericRepository
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class BaseUOW:
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self.session_factory = session_factory

    async def get_repository(
        self, MODEL: SQLALCHEMY_MODEL_TYPE, DTO: PYDANTIC_SCHEMA_TYPE
    ) -> GenericRepository[SQLALCHEMY_MODEL_TYPE, PYDANTIC_SCHEMA_TYPE]:
        class TempRepos(GenericRepository[MODEL, DTO]):
            pass

        return TempRepos(self.session_factory())
