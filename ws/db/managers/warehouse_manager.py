from ws.db.models import Warehouses, Items
from ws.dto import WarehousesDTO
from ws.db.managers.manager import BaseManager


class WarehousesManager(BaseManager):
    async def get_all(self) -> list[Warehouses]:
        return [
            warehouse for warehouse in await self.get_repository(Warehouses).get_batch()
        ]

    async def get_warehouse(self, **kwargs) -> WarehousesDTO:
        warehouse = await self.get_repository(Warehouses).get(**kwargs)
        return WarehousesDTO.from_instance(warehouse)

    async def get_warehouse_items(self, request_data: dict):
        repo = self.get_repository(Warehouses)
        repo.find().by().attach().attach()
