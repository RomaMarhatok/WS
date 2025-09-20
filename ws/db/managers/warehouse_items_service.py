from ws.db.managers.manager import BaseManager
from ws.db.models import WarehouseItems, Items
from ws.dto import ItemDTO


class WarehouseItemsManager(BaseManager):

    async def get_warehouse_items(self, **kwargs) -> list[ItemDTO]:
        joined_warehouse_items_repository = self.get_join_repository(
            WarehouseItems, Items
        )
