from random import choice
from ws.test.fixtures.factories import BaseFactory
from ws.test.fixtures.factories.items import ItemsFactory
from ws.db.models import WarehouseItems, Items, Warehouses


class WarehouseItemsFactory(BaseFactory):
    def __init__(self, session_factory):
        super().__init__(session_factory)

    @property
    def model(self):
        return WarehouseItems

    async def create(self):
        first_warehouse_id = self.get_model_cached_ids(Warehouses.__tablename__)[0]
        first_warehouse = [
            self.model(
                warehouses_uuididf=first_warehouse_id,
                item_uuididf=choice(
                    self.get_model_cached_ids(Items.__tablename__)[
                        : len(ItemsFactory.item_names) // 2
                    ]
                ),
                amount=self._get_random_number(0, 100),
            )
            for _ in range(5)
        ]
        second_warehouse = [
            self.model(
                warehouses_uuididf=list(
                    self.get_model_cached_ids()[Warehouses.__tablename__]
                )[1],
                item_uuididf=choice(
                    list(
                        self.get_model_cached_ids([Items.__tablename__])[
                            (len(ItemsFactory.item_names) // 2) + 1 :
                        ]
                    ),
                    amount=self._get_random_number(0, 100),
                ),
            )
            for _ in range(5)
        ]
        warehouses = first_warehouse + second_warehouse
        await self.save_instances(warehouses)
