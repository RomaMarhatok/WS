from ws.config import NeonDBConfig
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    async_sessionmaker,
    AsyncSession,
)


def get_sqlalchemy_async_engine() -> AsyncEngine:
    return create_async_engine(
        NeonDBConfig.DB_URL,
    )


def get_session_factory() -> async_sessionmaker[AsyncSession]:
    async_neon_engine = get_sqlalchemy_async_engine()
    session_factory = async_sessionmaker(
        bind=async_neon_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    return session_factory
