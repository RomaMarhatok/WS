import os
import sys
import asyncio
import pytest
import pytest_asyncio
from dotenv import load_dotenv
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    async_sessionmaker,
    AsyncSession,
)
from sqlalchemy.pool import NullPool
from ws.db.session import get_session_factory

load_dotenv(override=True)
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@pytest_asyncio.fixture(scope="session")
async def neon_db_url() -> str:
    return os.environ["NEON_DB_URL"]


@pytest_asyncio.fixture(scope="session")
async def neon_db_url_for_test():
    return os.environ["NEON_TEST_URL"]


@pytest.fixture(scope="session")
def async_session_maker():
    return get_session_factory()


@pytest.fixture(scope="session")
def async_session_maker_for_test(neon_db_url_for_test):
    engine = create_async_engine(neon_db_url_for_test, poolclass=NullPool, echo=True)
    session_factory = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    return session_factory


@pytest_asyncio.fixture(scope="session")
async def neon_async_engine(neon_db_url) -> AsyncGenerator[AsyncEngine, None]:
    engine = create_async_engine(neon_db_url)
    yield engine
    await engine.dispose()
