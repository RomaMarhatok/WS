from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from ws.db.commands import UserCommandsManager


class BaseUOW:
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self._model = None
        self.session_factory = session_factory

    @property
    def users(self):
        return UserCommandsManager(self.session_factory())
