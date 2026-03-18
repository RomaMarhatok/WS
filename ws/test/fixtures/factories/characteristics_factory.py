from ws.test.fixtures.factories import BaseFactory
from ws.db.models.characteristics import Characteristics


class CharacteristicsFactory(BaseFactory[Characteristics]):

    def __init__(self, db):
        super().__init__(db)

    @property
    def model(self):
        return Characteristics

    async def get_instances(self):
        characteristics_names = [
            "price",
            "size",
            "power",
            "brand",
            "release",
        ]
        return [self.model(name=name) for name in characteristics_names]
