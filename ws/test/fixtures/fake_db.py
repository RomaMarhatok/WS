from typing import Iterable
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from ws.test.fixtures.factories import BaseFactory
from ws.test.fixtures.factories.role_factory import RoleFactory
from ws.test.fixtures.factories.user_factory import UserFactory
from ws.test.fixtures.factories.item_types_factory import ItemTypesFactory
from ws.test.fixtures.factories.items import ItemsFactory
from ws.test.fixtures.factories.warehouse_factory import WarehouseFactory
from ws.test.fixtures.factories.warehouse_items_factory import WarehouseItemsFactory


class Generator:
    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        factories: Iterable[BaseFactory],
    ):
        self.session_factory = session_factory
        self.factories = factories

    async def generate_db_data(self):
        for factory in self.factories:
            await self.launch_factory_generation(factory)

    async def launch_factory_generation(self, factory: type[BaseFactory]):
        await factory(self.session_factory).create()


async def fake_db_init(session_factory: async_sessionmaker[AsyncSession]):
    generator = Generator(
        session_factory=session_factory,
        factories=[
            RoleFactory,
            UserFactory,
            ItemTypesFactory,
            ItemsFactory,
            WarehouseFactory,
            WarehouseItemsFactory,
        ],
    )
    await generator.generate_db_data()
