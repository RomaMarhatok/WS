from ws.config import AbstractDBConfig
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    async_sessionmaker,
    AsyncSession,
)
from sqlalchemy.pool import NullPool


def get_async_engine(db_config: AbstractDBConfig) -> AsyncEngine:
    return create_async_engine(
        db_config.get_connection_string(), poolclass=NullPool, echo=True
    )


def get_session_factory(
    db_config: AbstractDBConfig,
) -> async_sessionmaker[AsyncSession]:
    async_engine = get_async_engine(db_config=db_config)
    session_factory = async_sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    return session_factory
