import pytest
from ws.db.repository.joined_repoistory import JoinedRepository
from ws.db.models import WarehouseItems, Items, ItemTypes


@pytest.fixture(scope="session")
def joined_repository(migrated_async_session_factory):
    class Repo(JoinedRepository):
        def __init__(self, async_sesssion_factory, models_to_join):
            super().__init__(async_sesssion_factory, models_to_join)

    return Repo(migrated_async_session_factory, [WarehouseItems, Items, ItemTypes])


def test_creation_joined_repository(migrated_async_session_factory):
    class Repo(JoinedRepository):
        def __init__(self, async_sesssion_factory, models_to_join):
            super().__init__(async_sesssion_factory, models_to_join)

    assert Repo(migrated_async_session_factory, [WarehouseItems, Items, ItemTypes])


@pytest.mark.asyncio
async def test_stmt_creation(joined_repository: JoinedRepository):
    stmt = await joined_repository._stmt(
        [WarehouseItems.amount, Items.uuididf], WarehouseItems.uuididf == Items.uuididf
    )
    assert stmt
