from ws.test.fixtures.factories import BaseFactory
from ws.db.models import ItemTypes


class ItemTypesFactory(BaseFactory):
    def __init__(self, session_factory):
        super().__init__(session_factory)
        self.item_types = ["pipes", "gears", "printers"]

    @property
    def model(self) -> ItemTypes:
        return ItemTypes

    async def create(self) -> None:
        items = [ItemTypes(name=item_type_name) for item_type_name in self.item_types]
        ids = await self.save_instances(items)
        self.models_cache_ids.update({self.model.__tablename__: ids})
