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
async def test_find_one_isntance(
    repository_role_fixture: "GenericRepository[Roles]",
):
    roles_batch = await repository_role_fixture.get_batch()
    role_uuididfs = [roles_batch[0].uuididf]
    roles_name = await repository_role_fixture.find(
        Roles.uuididf.in_(role_uuididfs), selected_fields=tuple([Roles.rolename])
    )
    print(roles_name)
    assert len(roles_name) == 1


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
async def test_call_flat_find(
    repository_role_fixture: "GenericRepository[Roles]",
):
    roles_batch = await repository_role_fixture.get_batch()
    role_uuididfs = [roles_batch[0].uuididf, roles_batch[1].uuididf]
    flat_find_result = await repository_role_fixture.find(
        Roles.uuididf.in_(role_uuididfs),
        selected_fields=tuple([Roles.rolename, Roles.created_at, Roles.uuididf]),
        get_flat_result=True,
    )
    assert len(flat_find_result) == 6


@pytest.mark.asyncio
async def test_get_flat_first_find(
    repository_role_fixture: "GenericRepository[Roles]",
):
    roles_batch = await repository_role_fixture.get_batch()
    role_uuididfs = [roles_batch[0].uuididf, roles_batch[1].uuididf]
    (
        rolename,
        created_at,
        uuididf,
    ) = await repository_role_fixture.find(
        Roles.uuididf.in_(role_uuididfs),
        selected_fields=tuple([Roles.rolename, Roles.created_at, Roles.uuididf]),
        get_flat_result=True,
        get_first=True,
    )
    assert roles_batch[0].rolename == rolename
    assert roles_batch[0].created_at == created_at
    assert roles_batch[0].uuididf == uuididf


@pytest.mark.asyncio
async def test_call_flat_find_with_get_first(
    repository_role_fixture: "GenericRepository[Roles]",
):
    roles_batch = await repository_role_fixture.get_batch()
    role_uuididfs = [roles_batch[0].uuididf, roles_batch[1].uuididf]
    (rolename,) = await repository_role_fixture.find(
        Roles.uuididf.in_(role_uuididfs),
        selected_fields=tuple([Roles.rolename]),
        get_flat_result=True,
        get_first=True,
    )

    assert isinstance(rolename, str)


@pytest.mark.asyncio
async def test_call_flat_find_without_passing_selected_fields(
    repository_role_fixture: "GenericRepository[Roles]",
):
    roles_batch = await repository_role_fixture.get_batch()
    role_uuididfs = [roles_batch[0].uuididf, roles_batch[1].uuididf]
    with pytest.raises(ValueError):
        await repository_role_fixture.find(
            Roles.uuididf.in_(role_uuididfs),
            get_flat_result=True,
        )


@pytest.mark.asyncio
async def test_find_not_exist_entities(
    repository_role_fixture: "GenericRepository[Roles]",
    not_exist_uuid: uuid.UUID = uuid.uuid4(),
):
    roles = await repository_role_fixture.find(Roles.uuididf == not_exist_uuid)
    assert len(roles) == 0
