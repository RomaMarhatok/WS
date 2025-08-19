import pytest
from alembic.command import upgrade
from alembic.config import Config
from alembic.runtime.migration import MigrationContext
from alembic.autogenerate import compare_metadata
from sqlalchemy import Connection
from sqlalchemy.ext.asyncio import AsyncEngine
from ws.db.models import BaseModel


@pytest.mark.asyncio
async def test_migrations_up_to_date(
    alembic_config_for_production_db: Config,
    get_sqlalchemy_async_engine_for_production_db: AsyncEngine,
):

    def test_migrations(conn: Connection):
        upgrade(alembic_config_for_production_db, "head")
        migration_ctx = MigrationContext.configure(conn)
        diff = compare_metadata(migration_ctx, BaseModel.metadata)
        return diff

    async with get_sqlalchemy_async_engine_for_production_db.connect() as conn:
        diff = await conn.run_sync(test_migrations)
        assert not diff
