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
async def test_get_instance(repository_role_fixture: "GenericRepository[Roles]"):
    roles = await repository_role_fixture.get_batch()
    role = await repository_role_fixture.get(roles[0].uuididf)
    async with repository_role_fixture.session_factory() as session:
        role = await session.merge(role)
    assert role is not None
    assert roles[0].uuididf == role.uuididf


@pytest.mark.asyncio
async def test_get_with_error(
    repository_role_fixture: "GenericRepository[Roles]",
    not_exist_uuid: uuid.UUID = uuid.uuid4(),
):
    with pytest.raises(EntityNotFoundException):
        await repository_role_fixture.get(not_exist_uuid)
