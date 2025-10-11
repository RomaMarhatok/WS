import pytest
import uuid
from typing import TYPE_CHECKING
from ws.db.models import Roles, Users
from ws.dto import RoleDTO, UserDTO
from ws.db.repository.exceptions import EntityNotFoundException, ForeignKeyNotExist

if TYPE_CHECKING:
    from ws.db.repository import GenericRepository


@pytest.mark.asyncio
async def test_update(repository_role_fixture: "GenericRepository[Roles]"):
    roles = await repository_role_fixture.get_batch()
    dto = RoleDTO.from_instance(roles[0])
    dto.rolename = "new-name"
    role = await repository_role_fixture.update(dto)
    assert role.rolename == dto.rolename
    assert len(roles) == len(await repository_role_fixture.get_batch())


@pytest.mark.asyncio
async def test_update_not_exist_entity(
    repository_role_fixture: "GenericRepository[Roles]",
):
    role = RoleDTO(uuididf=uuid.uuid4(), rolename="not-exist")
    with pytest.raises(EntityNotFoundException):
        await repository_role_fixture.update(role)


@pytest.mark.asyncio
async def test_update_on_foreignkey_wich_not_exist(
    repository_user_fixture: "GenericRepository[Users]",
):
    user = (await repository_user_fixture.get_batch(limit=1))[0]
    user.role_uuididf = uuid.uuid4()
    dto = UserDTO.from_instance(user)
    with pytest.raises(ForeignKeyNotExist):
        await repository_user_fixture.update(dto)
