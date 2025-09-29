from abc import ABC
from sqlalchemy import Select
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.attributes import InstrumentedAttribute
from ws.db.repository.reflectors.fk_reflector import FkReflector
from ws.db.repository.reflectors.combinable_tables import CombinableList
from collections.abc import Iterable
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from ws.db.types import SQLALCHEMY_MODEL_TYPE


class Query:
    def __init__(self):
        self.stmt = None


class JoinedRepository(ABC):
    def __init__(
        self,
        async_session_factory: async_sessionmaker[AsyncSession],
        fk_reflector: FkReflector,
        models_list: CombinableList,
        selected_from_model: type[SQLALCHEMY_MODEL_TYPE],
    ):

        self.async_session_factory = async_session_factory
        self.fk_reflector = fk_reflector

        self.models_list = models_list
        self.selected_from = selected_from_model

    @classmethod
    async def init(
        cls,
        selected_from_model: type[SQLALCHEMY_MODEL_TYPE],
        async_session_factory: async_sessionmaker[AsyncSession],
        models_to_join: list[type[SQLALCHEMY_MODEL_TYPE]],
    ):
        models_to_join.insert(0, selected_from_model)
        refl = FkReflector(
            async_session_factory, [m.__tablename__ for m in models_to_join]
        )
        fks_reflection = await refl.get_fks_reflection()
        models_list = CombinableList(fks_reflection, models_to_join)
        return cls(async_session_factory, refl, models_list, selected_from_model)

    async def _build_join(self):
        stmt = None

    async def _build_options(self):
        pass

    async def _build_filters(self):
        pass

    async def _compile_select_stmt(
        self,
        selectable: Iterable[InstrumentedAttribute | type[SQLALCHEMY_MODEL_TYPE]],
        *where_clasue,
    ) -> Select:
        pass
        # stmt = Select(*selectable).select_from(self.selected_from)
        # pairs = self.models_list.devide_tables_by_pairs()
        # for (
        #     connectable_model,
        #     connected_model,
        # ) in pairs:

        #     stmt = stmt.join(
        #         connected_model,
        #         await self.fk_reflector.get_field_to_which_connect(
        #             connectable_model, connected_model.__tablename__
        #         )
        #         == getattr(connected_model, "uuididf"),
        #     )
        # stmt = stmt.join(
        #     self.selected_from,
        #     await self.fk_reflector.get_field_to_which_connect(
        #         self.models_list[0], self.selected_from.__tablename__
        #     )
        #     == getattr(self.selected_from, "uuididf"),
        # )

        # return stmt
