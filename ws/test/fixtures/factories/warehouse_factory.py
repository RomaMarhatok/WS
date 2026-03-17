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
        warehouses = [
            self.model(
                warehouse_name=name,
                warehouse_worker_uuididf=choice(
                    list(self.get_model_cached_ids(Users.__tablename__))
                ),
            )
            for name in self.warehouse_names
        ]
        warehouse_ids = await self.save_instances(warehouses)
        self.models_cache_ids.get({self.model.__tablename__: warehouse_ids})
