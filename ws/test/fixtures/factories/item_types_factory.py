from ws.test.fixtures.factories import BaseFactory
from ws.db.models import ItemTypes


class ItemTypesFactory(BaseFactory):
    def __init__(self, session_factory):
        super().__init__(session_factory)

    @property
    def model(self) -> ItemTypes:
        return ItemTypes

    async def get_instances(self):
        item_types = ["pipes", "gears", "printers"]
        return [ItemTypes(name=item_type_name) for item_type_name in item_types]
