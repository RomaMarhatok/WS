# libs
import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

# app
from ws.db.repository import UserRepository
from ws.dto.user import UserCreationDTO


@pytest.fixture(scope="module")
def user_repo(
    async_session_factory: async_sessionmaker[AsyncSession],
) -> UserRepository:
    return UserRepository(async_session_factory)


@pytest.fixture(scope="module")
def user_payload() -> UserCreationDTO:
    pass


@pytest.mark.asyncio
async def test_user_creation(user_repo: UserRepository):
    pass
