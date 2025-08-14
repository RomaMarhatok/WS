import pytest
from sqlalchemy import text
from ws.db.session import get_sqlalchemy_async_engine


@pytest.mark.asyncio
async def test_create_sqlalchemy_engine_for_neon_db():
    engine = get_sqlalchemy_async_engine()
    print(engine.url)
    async with engine.connect() as conn:
        result = await conn.execute(text("select 'HELLO WORLD'"))
        s = result.scalar()
        assert s == "HELLO WORLD"
        await engine.dispose()
