import pytest
from typing import TYPE_CHECKING
from ws.db.models import Roles
from ws.dto import RoleDTO

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
