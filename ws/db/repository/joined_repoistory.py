from abc import ABC
from collections.abc import Iterable
from sqlalchemy import Select
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from ws.db.repository.reflectors.fk_reflector import FkReflector
from ws.db.types import SQLALCHEMY_MODEL_TYPE
from ws.db.repository.reflectors.combinable_tables import CombinableList
from ws.utils.func import async_to_sync


class JoinedRepository(ABC):
    def __init__(
        self,
        async_sesssion_factory: async_sessionmaker[AsyncSession],
        models_to_join: list[type[SQLALCHEMY_MODEL_TYPE]],
    ):

        self.async_sesssion_factory = async_sesssion_factory
        self.fk_reflector = FkReflector(
            self.async_sesssion_factory,
            tablename_filter=models_to_join,
        )
        self.models_list = CombinableList(
            async_to_sync(self.fk_reflector.get_fks_reflection),
            models_to_join,
        )

    async def _create_filters(
        self, model: type[SQLALCHEMY_MODEL_TYPE], **kwargs
    ) -> list:
        if len(kwargs.items()) == 0:
            raise ValueError("Expected at least on keyword argument")
        filters = set()
        for k, v in kwargs.items():
            try:
                filters.add(getattr(model, k) == v)
            except AttributeError:
                raise AttributeError(
                    f"Model {model.__name__} doesn't have how field '{k}'"
                )
        return filters

    async def _stmt(
        self,
        selectable: Iterable[InstrumentedAttribute | type[SQLALCHEMY_MODEL_TYPE]],
        *args,
    ):
        stmt = Select(*selectable)
        pairs = self.models_list.devide_tables_by_pairs()
        for (
            connectable_model,
            connected_model,
        ) in pairs:
            stmt = stmt.join(
                connected_model,
                await self.fk_reflector.get_field_to_which_connect(
                    connectable_model, connected_model.__tablename__
                )
                == getattr(connected_model, "uuididf"),
            )
        stmt = stmt.where(*args)
        return stmt
