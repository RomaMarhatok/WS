from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from ws.db.commands import UserCommandsManager, WarehousesCommands


class BaseUOW:
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self.session_factory = session_factory

    @property
    def users(self):
        return UserCommandsManager(self.session_factory)

    @property
    def warehouses(self):
        return WarehousesCommands(self.session_factory)
