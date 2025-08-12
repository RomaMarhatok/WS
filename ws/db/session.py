from ws.config import NeonDBConfig
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine


def get_sqlalchemy_async_engine() -> AsyncEngine:
    return create_async_engine(
        NeonDBConfig.DB_URL,
    )
