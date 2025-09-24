import pytest
from ws.db.managers import WarehouseItemsManager, WarehousesManager


@pytest.fixture(scope="session")
def warehouse_items_manager(db_session_factory):
    return WarehouseItemsManager(db_session_factory)


@pytest.fixture(scope="session")
def warehouse_manager(db_session_factory):
    return WarehousesManager(db_session_factory)


@pytest.mark.asyncio
async def test_find_method(
    warehouse_items_manager: WarehouseItemsManager,
    warehouse_manager: WarehousesManager,
):
    warehouses = (await warehouse_manager.get_all())[0]

    await warehouse_items_manager.get_warehouse_items(**warehouses.model_dump())
