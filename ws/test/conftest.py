import pytest
import pytest_asyncio
import asyncio
from typing import AsyncGenerator
from dotenv import load_dotenv
from alembic.config import Config
from alembic.command import upgrade, downgrade
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, AsyncSession
from ws.db.session import get_session_factory, get_async_engine
from ws.config import DBConnectionStringController, AbcUrlDbConfig
from ws.utils.alembic_utils import alembic_config_from_url
from ws.test.fixtures.fake_db import fake_db_init

load_dotenv(override=True)


@pytest.fixture(scope="session")
def db_config() -> AbcUrlDbConfig:
    return DBConnectionStringController().get_config()


@pytest_asyncio.fixture(scope="session")
async def async_engine(
    db_config: AbcUrlDbConfig,
) -> AsyncGenerator[AsyncEngine, None]:
    engine = get_async_engine(db_config)
    yield engine
    await engine.dispose()


@pytest.fixture(scope="session")
def async_session_factory(
    db_config: AbcUrlDbConfig,
) -> async_sessionmaker[AsyncSession]:
    return get_session_factory(db_config)


@pytest.fixture(scope="session")
def alembic_config(db_config: AbcUrlDbConfig) -> Config:
    return alembic_config_from_url(db_url=db_config.get_connection_string())


@pytest_asyncio.fixture(scope="session")
async def migrated_async_session_factory(db_config: AbcUrlDbConfig, alembic_config):
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, upgrade, alembic_config, "head")
    yield get_session_factory(db_config)
    await loop.run_in_executor(None, downgrade, alembic_config, "base")


@pytest_asyncio.fixture(scope="session")
async def db_session_factory(migrated_async_session_factory):
    await fake_db_init(migrated_async_session_factory)
    yield migrated_async_session_factory
