from random import choice
from ws.test.fixtures.factories import BaseFactory
from ws.db.models import WarehouseItems, Items, Warehouses


class WarehouseItemsFactory(BaseFactory):
    def __init__(self, session_factory):
        super().__init__(session_factory)

    @property
    def model(self):
        return WarehouseItems

    async def create(self):
        uuididfs = list(self.generate_uuid_collection(self.model.__tablename__, 10))
        first_warehouse = [
            self.model(
                uuididf=uuididf,
                warehouses_uuididf=list(
                    self.get_collection().get(Warehouses.__tablename__)
                )[0],
                item_uuididf=choice(
                    list(self.get_collection().get(Items.__tablename__))
                ),
                amount=self._get_random_number(0, 100),
            )
            for uuididf in uuididfs[:5]
        ]
        second_warehouse = [
            self.model(
                uuididf=uuididf,
                warehouses_uuididf=list(
                    self.get_collection()[Warehouses.__tablename__]
                )[1],
                item_uuididf=choice(list(self.get_collection()[Items.__tablename__])),
                amount=self._get_random_number(0, 100),
            )
            for uuididf in uuididfs[5:]
        ]
        warehouses = first_warehouse + second_warehouse
        await self.save_instances(warehouses)
