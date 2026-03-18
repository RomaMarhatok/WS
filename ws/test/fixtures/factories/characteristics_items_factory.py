from ws.test.fixtures.factories import BaseFactory
from ws.db.models.characteristics_items import CharacteristicsItems


class CharacteristicsFactory(BaseFactory[CharacteristicsItems]):

    def __init__(self, db):
        super().__init__(db)

    @property
    def model(self):
        return CharacteristicsItems

    async def get_instances(self):
        pass
