from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    async_sessionmaker,
    AsyncSession,
)
from sqlalchemy.pool import NullPool
from config import UrlCreatorProtocol


def get_async_engine(db_config: UrlCreatorProtocol) -> AsyncEngine:
    return create_async_engine(db_config.db_url, poolclass=NullPool, echo=True)


def get_async_session_factory(
    db_config: UrlCreatorProtocol,
) -> async_sessionmaker[AsyncSession]:
    async_engine = get_async_engine(db_config)
    session_factory = async_sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    return session_factory
