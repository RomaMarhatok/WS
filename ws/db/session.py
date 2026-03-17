from typing import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession

from ws.core.config import DbConfProtocol, app_config


class SessionManager:

    def __init__(self, db_config: DbConfProtocol):
        self.conf = db_config

    async def get_async_engine(
        self, conf: DbConfProtocol = None
    ) -> AsyncGenerator[AsyncEngine]:
        _conf = conf or self.conf
        eng = create_async_engine(_conf, poolclass=NullPool, echo=True)
        yield eng
        eng.dispose()

    @asynccontextmanager
    async def get_db_session(
        self, eng: AsyncEngine = None
    ) -> AsyncGenerator[AsyncSession]:
        _engine = eng or await anext(self.get_async_engine())
        async with AsyncSession(_engine) as session:
            yield session


def get_session_manager() -> SessionManager:
    return SessionManager(app_config)
