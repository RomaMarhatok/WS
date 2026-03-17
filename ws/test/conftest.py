import pytest
import pytest_asyncio

from ws.core.config import (
    app_config,
    AppConfig,
)
from ws.db.session import SessionManager
from ws.test.fixtures.fake_db import fake_db_init


@pytest.fixture(scope="session")
def db_config() -> AppConfig:
    return app_config


@pytest_asyncio.fixture(scope="session")
async def get_session_manager(
    db_conf: AppConfig,
) -> SessionManager:
    return SessionManager(db_conf.db_url)


@pytest_asyncio.fixture(scope="session")
async def db_session(session_manager: SessionManager):
    await fake_db_init(session_manager)
    yield session_manager
