import pytest
import uuid
from typing import TYPE_CHECKING
from ws.db.models import Roles
from ws.dto import RoleDTO
from ws.db.repository.exceptions import EntityAlreadyExistException

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
