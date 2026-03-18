from random import choice
from ws.db.models import Warehouses, Users
from ws.test.fixtures.factories import BaseFactory


class WarehouseFactory(BaseFactory):
    def __init__(self, session_factory):
        super().__init__(session_factory)

    @property
    def model(self):
        return Warehouses

    async def get_instances(self):
        warehouse_names = ["warehouse-1", "warehouse-2"]
        return [
            self.model(
                warehouse_name=name,
                warehouse_worker_id=choice(await self.get_model_ids(Users)),
            )
            for name in warehouse_names
        ]
