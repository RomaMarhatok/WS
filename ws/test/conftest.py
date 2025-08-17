import os
import sys
import asyncio
import pytest_asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
)

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@pytest_asyncio.fixture(scope="session")
async def neon_db_url() -> str:
    return os.environ["NEON_DB_URL"]


@pytest_asyncio.fixture(scope="session")
async def neon_async_engine(neon_db_url) -> AsyncGenerator[AsyncEngine, None]:
    engine = create_async_engine(neon_db_url)
    yield engine
    await engine.dispose()
