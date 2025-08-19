import pytest
import asyncio
from typing import Generator, Any
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from alembic.command import upgrade, downgrade
from alembic.config import Config
from ws.utils.alembic_utils import alembic_config_from_url
from sqlalchemy.pool import NullPool


@pytest.fixture(scope="session")
def async_session_maker_for_test(neon_db_url_for_test):
    engine = create_async_engine(neon_db_url_for_test, poolclass=NullPool, echo=True)
    session_factory = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    return session_factory


@pytest.fixture(scope="session")
def alembic_config_for_fake_db(neon_db_url_for_test) -> Generator[Any, Config]:
    yield alembic_config_from_url(db_url=neon_db_url_for_test, testing=True)


@pytest.fixture(scope="session")
def migrate_fake_migrations(alembic_config_for_fake_db: Config, neon_db_url_for_test):
    upgrade(alembic_config_for_fake_db, "head")
    yield
    from ws.test.test_repository.fake_db.fake_tables import FakeBaseModel

    async def _delete_record_from_db():
        engine = create_async_engine(
            neon_db_url_for_test, poolclass=NullPool, echo=True
        )
        async with engine.connect() as conn:
            await conn.run_sync(FakeBaseModel.metadata.drop_all)

    asyncio.run(_delete_record_from_db())
    downgrade(alembic_config_for_fake_db, "base")
