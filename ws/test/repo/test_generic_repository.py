import pytest
import pytest_asyncio
from ws.db.session import SessionManager
from ws.db.uow import UnitOfWork
from ws.db.repository import RoleRepository, UserRepository


@pytest_asyncio.fixture(scope="module")
async def role_repo(db_session: SessionManager):
    async with UnitOfWork(RoleRepository, db_session) as uow:
        yield uow.repo


@pytest_asyncio.fixture(scope="module")
async def user_repo(db_session: SessionManager):
    async with UnitOfWork(UserRepository, db_session) as uow:
        yield uow.repo


@pytest.mark.asyncio
async def test_get(role_repo: RoleRepository):
    role = await role_repo.get(1)
    assert role is not None


@pytest.mark.asyncio
async def test_get_with_exclude(role_repo: RoleRepository):
    pass
