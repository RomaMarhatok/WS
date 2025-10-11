import pytest
import uuid
from typing import TYPE_CHECKING
from ws.db.models import Roles
from sqlalchemy import and_

if TYPE_CHECKING:
    from ws.db.repository import GenericRepository


@pytest.mark.asyncio()
async def test_find(repository_role_fixture: "GenericRepository[Roles]"):
    roles_batch = await repository_role_fixture.get_batch()
    role_name = roles_batch[0].rolename
    role_uuididf = roles_batch[0].uuididf
    role = await repository_role_fixture.find(
        and_(
            Roles.rolename == role_name,
            Roles.uuididf == role_uuididf,
        ),
        get_first=True,
    )
    assert isinstance(role, Roles)


@pytest.mark.asyncio
async def test_find_list(repository_role_fixture: "GenericRepository[Roles]"):
    roles_batch = await repository_role_fixture.get_batch()
    role_uuididfs = [roles_batch[0].uuididf, roles_batch[1].uuididf]

    roles = await repository_role_fixture.find(
        Roles.uuididf.in_(role_uuididfs),
    )
    assert isinstance(roles, list)
    assert len(roles) != 0


@pytest.mark.asyncio
async def test_find_list_with_ine_selected_field(
    repository_role_fixture: "GenericRepository[Roles]",
):
    roles_batch = await repository_role_fixture.get_batch()
    role_uuididfs = [roles_batch[0].uuididf, roles_batch[1].uuididf]

    roles_name = await repository_role_fixture.find(
        Roles.uuididf.in_(role_uuididfs), selected_fields=tuple([Roles.rolename])
    )
    assert len(roles_name) == 2


@pytest.mark.asyncio
async def test_find_list_with_selected_fields(
    repository_role_fixture: "GenericRepository[Roles]",
):
    roles_batch = await repository_role_fixture.get_batch()
    role_uuididfs = [roles_batch[0].uuididf, roles_batch[1].uuididf]

    roles_name = await repository_role_fixture.find(
        Roles.uuididf.in_(role_uuididfs),
        selected_fields=tuple([Roles.rolename, Roles.created_at, Roles.uuididf]),
    )
    assert len(roles_name) == 2
    assert len(roles_name[0]) == 3


@pytest.mark.asyncio
async def test_find_not_exist_entities(
    repository_role_fixture: "GenericRepository[Roles]",
    not_exist_uuid: uuid.UUID = uuid.uuid4(),
):
    roles = await repository_role_fixture.find(Roles.uuididf == not_exist_uuid)
    assert len(roles) == 0
