import pytest
import pytest_asyncio
import asyncio
from dotenv import load_dotenv
from alembic.config import Config
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, AsyncSession
from ws.db.session import get_session_factory, get_async_engine
from ws.config import DBConnectionStringController, AbstractDBConfig
from ws.utils.alembic_utils import alembic_config_from_url
from alembic.command import upgrade, downgrade

load_dotenv(override=True)


@pytest.fixture(scope="session")
def db_config() -> AbstractDBConfig:
    return DBConnectionStringController().get_config()


@pytest_asyncio.fixture(scope="session")
async def async_engine(
    db_config: AbstractDBConfig,
) -> AsyncGenerator[AsyncEngine, None]:
    engine = get_async_engine(db_config)
    yield engine
    await engine.dispose()


@pytest.fixture(scope="session")
def async_session_factory(
    db_config: AbstractDBConfig,
) -> async_sessionmaker[AsyncSession]:
    return get_session_factory(db_config)


@pytest_asyncio.fixture(scope="session")
async def migrated_async_session_factory(db_config: AbstractDBConfig, alembic_config):
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, upgrade, alembic_config, "head")
    yield get_session_factory(db_config)
    await loop.run_in_executor(None, downgrade, alembic_config, "base")


@pytest.fixture(scope="session")
def alembic_config(db_config: AbstractDBConfig) -> Config:
    return alembic_config_from_url(db_url=db_config.get_connection_string())
