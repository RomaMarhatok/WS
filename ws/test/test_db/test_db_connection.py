import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine


@pytest.mark.asyncio
async def test_connection_with_db(
    async_engine: AsyncEngine,
):
    async with async_engine.connect() as conn:
        result = await conn.execute(text("select 'HELLO WORLD'"))
        s = result.scalar()
        assert s == "HELLO WORLD"
        await async_engine.dispose()
