import pytest
import uuid
from typing import TYPE_CHECKING
from ws.db.models import Users, Roles
from ws.db.repository.exceptions import (
    ForeignKeyRestrictException,
    EntityNotFoundException,
)

if TYPE_CHECKING:
    from ws.db.repository import GenericRepository


@pytest.mark.asyncio
async def test_delete_entity_without_foreign_keys_dependency(
    repository_user_fixture: "GenericRepository[Users]",
):
    users = await repository_user_fixture.get_batch(limit=1)
    is_deleted = await repository_user_fixture.delete(users[0])
    assert is_deleted


@pytest.mark.asyncio
async def test_delete_by_uuididf(repository_user_fixture: "GenericRepository[Users]"):
    users = await repository_user_fixture.get_batch(limit=1)
    is_deleted = await repository_user_fixture.delete(users[0].uuididf)
    assert is_deleted


@pytest.mark.asyncio
async def test_delete_not_exist_entity(
    repository_user_fixture: "GenericRepository[Users]",
):
    with pytest.raises(EntityNotFoundException):
        await repository_user_fixture.delete(uuid.uuid4())


@pytest.mark.asyncio
async def test_delete_entity_with_foreign_keys_dependency(
    repository_role_fixture: "GenericRepository[Roles]",
):

    roles = await repository_role_fixture.get_batch()
    with pytest.raises(ForeignKeyRestrictException):
        await repository_role_fixture.delete(roles[0])
