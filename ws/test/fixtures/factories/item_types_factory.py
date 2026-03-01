from ws.test.fixtures.factories import BaseFactory
from ws.db.models import ItemTypes


class ItemTypesFactory(BaseFactory):
    def __init__(self, session_factory):
        super().__init__(session_factory)
        self.item_types = ["pipes", "gears", "printers"]

    @property
    def model(self):
        return ItemTypes

    async def create(self):
        uuididfs = self.generate_uuid_collection(self.model.__tablename__, 3)
        items = [
            ItemTypes(uuididf=uuididf, name=item_type_name)
            for uuididf, item_type_name in zip(uuididfs, self.item_types)
        ]
        await self.save_instances(items)
