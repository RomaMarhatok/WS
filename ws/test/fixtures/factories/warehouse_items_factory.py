from random import choice
from ws.test.fixtures.factories import BaseFactory
from ws.db.models import WarehouseItems, Items, Warehouses


class WarehouseItemsFactory(BaseFactory):
    def __init__(self, session_factory):
        super().__init__(session_factory)

    @property
    def model(self):
        return WarehouseItems

    async def get_instances(self):
        warehouse_ids = await self.get_model_ids(Warehouses)
        items_ids = await self.get_model_ids(Items)
        first_warehouse = [
            self.model(
                warehouses_id=warehouse_ids[0],
                item_id=choice(items_ids[: len(items_ids) // 2]),
                amount=self._get_random_number(0, 100),
            )
            for _ in range(5)
        ]
        second_warehouse = [
            self.model(
                warehouses_id=warehouse_ids[1],
                item_id=choice(items_ids[len(items_ids) // 2 :]),
                amount=self._get_random_number(0, 100),
            )
            for _ in range(5)
        ]
        return first_warehouse + second_warehouse
