import os
import pytest
import pytest_asyncio
from dotenv import load_dotenv
from alembic.config import Config
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, AsyncSession
from ws.db.session import get_session_factory, get_async_engine
from ws.config import PSQLDBConfig, AbstractDBConfig
from ws.utils.alembic_utils import alembic_config_from_url

load_dotenv(override=True)


@pytest.fixture(scope="session")
def db_config() -> AbstractDBConfig:
    return PSQLDBConfig(
        DB_NAME=os.environ["TEST_DB_NAME"],
        DB_PORT=os.environ["DB_PORT_FOR_TEST"],
        DB_HOST=os.environ["TEST_DB_HOST"],
    )


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


@pytest.fixture(scope="session")
def alembic_config(db_config: AbstractDBConfig) -> Config:
    return alembic_config_from_url(db_url=db_config.get_connection_string())
