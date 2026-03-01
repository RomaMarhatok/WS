from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from ws.db.managers import UserManager, WarehousesManager


class BaseUOW:
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self.session_factory = session_factory

    @property
    def users(self):
        return UserManager(self.session_factory)

    @property
    def warehouses(self):
        return WarehousesManager(self.session_factory)
