import pytest
from typing import Any
from ws.db.models import (
    Warehouses,
    Items,
    CharacteristicsItems,
    Characteristics,
    WarehouseItems,
    ItemTypes,
)
from sqlalchemy.orm.relationships import RelationshipProperty
from ws.db.types import SQLALCHEMY_MODEL_TYPE


def normalize_dict(
    d: dict[type[SQLALCHEMY_MODEL_TYPE], list[RelationshipProperty[Any]]],
):
    return {model.__tablename__: [rel.key for rel in rels] for model, rels in d.items()}


@pytest.mark.asyncio
async def test_relationship_warehouse_tree_building():
    graph = Warehouses.get_relationships_graph()
    warehouse_graph = {
        Warehouses: [Warehouses.warehouse_items],
        Items: [Items.item_type, Items.item_characteristics],
        CharacteristicsItems: [
            CharacteristicsItems.characteristics,
            CharacteristicsItems.items,
        ],
        WarehouseItems: [WarehouseItems.warehouses, WarehouseItems.item],
        ItemTypes: [],
        Characteristics: [],
    }

    assert normalize_dict(graph) == normalize_dict(warehouse_graph)


@pytest.mark.asyncio
async def test_relationship_item_type_tree_building():
    graph = ItemTypes.get_relationships_graph()
    item_types_graph = {
        ItemTypes: [],
    }
    assert normalize_dict(graph) == normalize_dict(item_types_graph)
