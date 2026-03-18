from typing import Sequence
from random import choice

from ws.db.models import Items, ItemTypes
from ws.test.fixtures.factories import BaseFactory, fake


class ItemsFactory(BaseFactory):

    def __init__(self, session_factory):
        super().__init__(session_factory)

    @property
    def model(self) -> Items:
        return Items

    async def get_instances(self):
        item_names: Sequence[str] = [
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
        return [
            self.model(
                nomination=name,
                description=fake.text(max_nb_chars=20),
                type_id=choice(await self.get_model_ids(ItemTypes)),
            )
            for name in item_names
        ]
