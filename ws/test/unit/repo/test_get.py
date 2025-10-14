import pytest
import uuid
from typing import TYPE_CHECKING
from ws.db.models import Roles
from ws.db.repository.exceptions import EntityNotFoundException

if TYPE_CHECKING:
    from ws.db.repository import GenericRepository


@pytest.mark.asyncio()
async def test_get_batch(repository_role_fixture: "GenericRepository[Roles]"):
    limit_of_batch = 10
    amount_of_skipped_records = 1
    batch_of_roles = await repository_role_fixture.get_batch(
        limit=limit_of_batch, offset=amount_of_skipped_records
    )
    assert isinstance(batch_of_roles, list)
    assert 0 < len(batch_of_roles) <= limit_of_batch
    assert isinstance(batch_of_roles[0], Roles)


@pytest.mark.asyncio
async def test_get_batch_with_limit(
    repository_role_fixture: "GenericRepository[Roles]",
):
    batch_limit = 1
    roles = await repository_role_fixture.get_batch(limit=batch_limit)
    assert len(roles) == batch_limit


@pytest.mark.asyncio
async def test_get_instance(repository_role_fixture: "GenericRepository[Roles]"):
    roles = await repository_role_fixture.get_batch(limit=1)
    role = await repository_role_fixture.get(roles[0].uuididf)
    async with repository_role_fixture.session_factory() as session:
        role = await session.merge(role)
    assert role is not None
    assert roles[0].uuididf == role.uuididf


@pytest.mark.asyncio
async def test_get_with_sleect_one_field(
    repository_role_fixture: "GenericRepository[Roles]",
):
    roles = await repository_role_fixture.get_batch(limit=1)
    role = roles[0]
    rolename = await repository_role_fixture.get(role.uuididf, Roles.rolename)
    assert role.rolename == rolename


@pytest.mark.asyncio
async def test_get_with_selected_fields(
    repository_role_fixture: "GenericRepository[Roles]",
):
    roles = await repository_role_fixture.get_batch(limit=1)
    role = roles[0]
    result = await repository_role_fixture.get(
        role.uuididf, Roles.rolename, Roles.uuididf, Roles.created_at
    )
    assert len(result) == 1
    assert len(result[0]) == 3


@pytest.mark.asyncio
async def test_get_not_exist_entity(
    repository_role_fixture: "GenericRepository[Roles]",
    not_exist_uuid: uuid.UUID = uuid.uuid4(),
):
    with pytest.raises(EntityNotFoundException):
        await repository_role_fixture.get(not_exist_uuid)
