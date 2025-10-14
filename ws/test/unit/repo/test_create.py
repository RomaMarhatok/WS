import pytest
import uuid
from typing import TYPE_CHECKING
from ws.db.models import Roles, Users
from ws.dto import RoleDTO, UserDTO
from ws.db.repository.exceptions import EntityAlreadyExistException, ForeignKeyNotExist
from ws.utils.security import get_password_hash

if TYPE_CHECKING:
    from ws.db.repository import GenericRepository


@pytest.mark.asyncio
async def test_create_role(repository_role_fixture: "GenericRepository[Roles]"):
    count_of_roles = len(await repository_role_fixture.get_batch())
    role_dto = RoleDTO(uuididf=uuid.uuid4(), rolename="test-user")
    await repository_role_fixture.save(role_dto)
    assert (count_of_roles + 1) == len(await repository_role_fixture.get_batch())


@pytest.mark.asyncio
async def test_create_existed_role(repository_role_fixture: "GenericRepository[Roles]"):
    with pytest.raises(EntityAlreadyExistException):
        role_dto = RoleDTO(uuididf=uuid.uuid4(), rolename="test-user")
        await repository_role_fixture.save(role_dto)


@pytest.mark.asyncio
async def test_create_user(
    repository_role_fixture: "GenericRepository[Roles]",
    repository_user_fixture: "GenericRepository[Users]",
):
    roles = await repository_role_fixture.get_batch(limit=1)
    dto = UserDTO(
        uuididf=uuid.uuid4(),
        username="death_star2007",
        password=get_password_hash("1234password"),
        role_uuididf=roles[0].uuididf,
    )
    user = await repository_user_fixture.save(dto)
    assert user == dto


@pytest.mark.asyncio
async def test_create_user_with_not_exist_role_uuid(
    repository_user_fixture: "GenericRepository[Users]",
):
    dto = UserDTO(
        uuididf=uuid.uuid4(),
        username="suprime-commander",
        password=get_password_hash("1234password"),
        role_uuididf=uuid.uuid4(),
    )
    with pytest.raises(ForeignKeyNotExist):
        await repository_user_fixture.save(dto)
