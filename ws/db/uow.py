from ws.db.repository.generic_repository import GenericRepository
from ws.db.session import SessionManager


class UnitOfWork:
    def __init__(self, repo: GenericRepository, session_manager: SessionManager):
        self._repo = repo
        self.session_manager = session_manager
        self.session = None

    @property
    def repo(self) -> type[GenericRepository]:
        return self._repo(self.session)

    async def __aenter__(self):
        async with self.session_manager.get_db_session() as session:
            self.session = session
            return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.session:
            await self.session.close()
