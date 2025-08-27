import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from alembic.command import upgrade, downgrade
from alembic.config import Config
from sqlalchemy.pool import NullPool


@pytest.fixture(scope="session")
def apply_fake_migrations(alembic_config: Config, neon_db_url_for_test):
    upgrade(alembic_config, "head")
    yield

    async def _delete_record_from_db():
        from ws.db.models import BaseModel

        engine = create_async_engine(
            neon_db_url_for_test, poolclass=NullPool, echo=True
        )
        async with engine.connect() as conn:
            await conn.run_sync(BaseModel.metadata.drop_all)

    asyncio.run(_delete_record_from_db())
    downgrade(alembic_config, "base")
