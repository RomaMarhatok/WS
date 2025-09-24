from random import choice
from ws.db.models import Items, ItemTypes
from ws.test.fixtures.factories import BaseFactory, fake


class ItemsFactory(BaseFactory):
    def __init__(self, session_factory):
        super().__init__(session_factory)
        self.item_names = [
            "pipe-No123",
            "printer-#9393",
            "gear-1234/3134",
            "printer-1",
            "gear-6-ends",
            "pipeline-2",
            "gear-test",
            "secret-gear",
            "testing-pipes",
            "broke-gear",
        ]

    @property
    def model(self):
        return Items

    async def create(self):
        uuididfs = self.generate_uuid_collection(self.model.__tablename__, 10)
        items = [
            self.model(
                uuididf=uuididf,
                nomination=name,
                description=fake.text(max_nb_chars=20),
                type=choice(list(self.get_collection().get(ItemTypes.__tablename__))),
            )
            for uuididf, name in zip(uuididfs, self.item_names)
        ]
        await self.save_instances(items)
