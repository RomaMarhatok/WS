from ws.db.managers.manager import BaseManager
from ws.db import models
from ws.dto import ItemDTO


class WarehouseItemsManager(BaseManager):

    async def get_warehouse_items(self, **kwargs) -> list[ItemDTO]:
        join_repos = await self.get_join_repository(
            [models.WarehouseItems, models.Items, models.ItemTypes]
        )
        items = await join_repos.find(
            models.Warehouses,
            [models.Items, models.ItemTypes],
            **kwargs,
        )
        return items
