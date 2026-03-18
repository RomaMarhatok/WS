from datetime import datetime
import pytest

from ws.db.models import Roles
from ws.db.session import SessionManager
from ws.db.uow import UnitOfWork
from ws.db.repository import RoleRepository, UserRepository
from ws.api.v1.routers.exceptions import NotFoundError, ConflictError
from ws.api.v1.schemas.role import CreateRoleDTO, RoleNameEnum


@pytest.fixture(scope="function")
async def role_repo(db_session: SessionManager):
    async with UnitOfWork(RoleRepository, db_session) as uow:
        yield uow.repo


@pytest.fixture(scope="function")
async def user_repo(db_session: SessionManager):
    async with UnitOfWork(UserRepository, db_session) as uow:
        yield uow.repo


@pytest.mark.asyncio
async def test_get_role_by_id(role_repo: RoleRepository):
    role = await role_repo.get(1)
    assert isinstance(role.rolename, str)
    assert isinstance(role.created_at, datetime)
    assert isinstance(role.updated_at, datetime)


@pytest.mark.asyncio
async def test_get_role_with_note_exist_id(role_repo: RoleRepository):
    with pytest.raises(NotFoundError):
        await role_repo.get(-1)


@pytest.mark.asyncio
async def test_get_all(role_repo: RoleRepository):
    roles = await role_repo.get_batch()
    assert len(roles) == 2


@pytest.mark.asyncio
async def test_get_by_field(role_repo: RoleRepository):
    role = await role_repo.get_by_column(rolename=RoleNameEnum.ADMIN.value)
    assert isinstance(role.rolename, str)
    assert isinstance(role.created_at, datetime)
    assert isinstance(role.updated_at, datetime)


@pytest.mark.asyncio
async def test_get_batch(role_repo: RoleRepository):
    roles = await role_repo.get_batch()
    assert len(roles) != 0
    assert isinstance(roles[0], Roles)


@pytest.mark.asyncio
async def test_create_role(role_repo: RoleRepository, create_role_dto: CreateRoleDTO):
    before_creation = len(await role_repo.get_batch())
    await role_repo.create(create_role_dto)
    after_creation = len(await role_repo.get_batch())
    assert (after_creation - before_creation) == 1


@pytest.mark.asyncio
async def test_delete_role_without_users(
    role_repo: RoleRepository, create_role_dto: CreateRoleDTO
):
    role = await role_repo.create(create_role_dto)
    before_deletion = len(await role_repo.get_batch())
    await role_repo.delete(role.id)
    after_deletion = len(await role_repo.get_batch())
    assert before_deletion - after_deletion == 1
    with pytest.raises(NotFoundError):
        await role_repo.get(role.id)


@pytest.mark.asyncio
async def test_delete_role_with_user(role_repo: RoleRepository):
    with pytest.raises(ConflictError):
        await role_repo.delete(1)
