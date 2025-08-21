import pytest
import os
from alembic.config import Config
from ws.utils.alembic_utils import alembic_config_from_url
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
)
from sqlalchemy.pool import NullPool


@pytest.fixture(scope="session")
def alembic_config_for_production_db(neon_db_url) -> Config:
    return alembic_config_from_url(db_url=neon_db_url)


@pytest.fixture(scope="session")
def get_sqlalchemy_async_engine_for_production_db() -> AsyncEngine:
    return create_async_engine(os.environ["NEON_DB_URL"], poolclass=NullPool, echo=True)
