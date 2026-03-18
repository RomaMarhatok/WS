import pytest
from faker import Faker
from ws.core.config import (
    app_config,
    AppConfig,
)
from ws.db.session import SessionManager
from ws.test.fixtures.fake_db import fake_db_init, drop_fake_db


@pytest.fixture(scope="session")
def db_conf() -> AppConfig:
    return app_config


@pytest.fixture(scope="session")
async def session_manager(
    db_conf: AppConfig,
) -> SessionManager:
    return SessionManager(db_conf)


@pytest.fixture(scope="session")
async def db_session(session_manager: SessionManager):
    await fake_db_init(session_manager)
    yield session_manager
    await drop_fake_db(session_manager)


@pytest.fixture(scope="session")
async def fake_data_generator() -> Faker:
    return Faker()
