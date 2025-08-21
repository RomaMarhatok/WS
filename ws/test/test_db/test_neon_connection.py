import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine


@pytest.mark.asyncio
async def test_create_sqlalchemy_engine_for_neon_db(
    get_sqlalchemy_async_engine_for_production_db: AsyncEngine,
):
    engine = get_sqlalchemy_async_engine_for_production_db
    async with engine.connect() as conn:
        result = await conn.execute(text("select 'HELLO WORLD'"))
        s = result.scalar()
        assert s == "HELLO WORLD"
        await engine.dispose()
