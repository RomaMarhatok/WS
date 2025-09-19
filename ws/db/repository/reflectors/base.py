from sqlalchemy import Connection, inspect, Inspector
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class BaseReflector:

    def __init__(self, async_session_factory: async_sessionmaker[AsyncSession]):
        self.async_session_factory = async_session_factory

    def _create_inspector(sync_conn: Connection) -> Inspector:
        return inspect(sync_conn)
