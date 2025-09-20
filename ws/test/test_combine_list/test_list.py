import pytest
from ws.db.repository.reflectors.combinable_tables import CombinableList
from ws.db.repository.reflectors.fk_reflector import FkReflector
from ws.db.models import WarehouseItems, Items, ItemTypes
from ws.db.repository.exceptions import (
    NotCombinedTablesException,
)


@pytest.fixture(scope="session")
def fk_refl(migrated_async_session_factory):
    return FkReflector(
        migrated_async_session_factory,
        [WarehouseItems, Items, ItemTypes],
    )


@pytest.mark.asyncio
async def test_creation(fk_refl: FkReflector):
    reflection = await fk_refl.get_fks_reflection()
    instance = CombinableList(reflection, [WarehouseItems, Items])
    assert instance


@pytest.mark.asyncio
async def test_creation_with_not_correct_order(fk_refl: FkReflector):
    reflection = await fk_refl.get_fks_reflection()
    with pytest.raises(NotCombinedTablesException):
        CombinableList(reflection, [Items, WarehouseItems])


@pytest.mark.asyncio
async def test_creation_with_not_related_models(fk_refl: FkReflector):
    reflection = await fk_refl.get_fks_reflection()
    with pytest.raises(NotCombinedTablesException):
        CombinableList(reflection, [WarehouseItems, ItemTypes])


@pytest.mark.asyncio
async def test_ceration_with_complex_relation(fk_refl: FkReflector):
    reflection = await fk_refl.get_fks_reflection()
    instance = CombinableList(reflection, [WarehouseItems, Items, ItemTypes])
    assert instance


@pytest.mark.asyncio
async def test_devide_by_pairs(fk_refl: FkReflector):
    reflection = await fk_refl.get_fks_reflection()
    instance = CombinableList(reflection, [WarehouseItems, Items, ItemTypes])
    assert instance.devide_tables_by_pairs() == list(
        [(WarehouseItems, Items), (Items, ItemTypes)]
    )
