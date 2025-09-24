from random import choice
from ws.db.models import Warehouses, Users
from ws.test.fixtures.factories import BaseFactory


class WarehouseFactory(BaseFactory):
    def __init__(self, session_factory):
        super().__init__(session_factory)
        self.warehouse_names = ["warehouse-1", "warehouse-2"]

    @property
    def model(self):
        return Warehouses

    async def create(self):
        uuididfs = self.generate_uuid_collection(self.model.__tablename__, 2)
        warehouses = [
            self.model(
                uuididf=uuididf,
                warehouse_name=name,
                warehouse_worker_uuididf=choice(
                    list(self.get_collection().get(Users.__tablename__))
                ),
            )
            for uuididf, name in zip(uuididfs, self.warehouse_names)
        ]
        await self.save_instances(warehouses)
