from ws.db.models import Warehouses
from ws.dto import WarehousesDTO
from ws.db.managers.manager import BaseManager


class WarehousesManager(BaseManager):
    async def get_all(self, limit: int, offset: int) -> list[WarehousesDTO]:
        return [
            WarehousesDTO.from_instance(warehouse)
            for warehouse in await self.get_repository(Warehouses).get_batch(
                limit=limit, offset=offset
            )
        ]

    async def get_warehouse(self, **kwargs) -> WarehousesDTO:
        warehouse = await self.get_repository(Warehouses).get(**kwargs)
        return WarehousesDTO.from_instance(warehouse)
