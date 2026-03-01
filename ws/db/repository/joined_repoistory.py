from abc import ABC
from sqlalchemy import Select
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.attributes import InstrumentedAttribute
from ws.db.repository.reflectors.fk_reflector import FkReflector
from ws.db.repository.reflectors.combinable_tables import CombinableList
from collections.abc import Iterable
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from ws.db.types import SQLALCHEMY_MODEL_TYPE


class JoinedRepository(ABC):
    def __init__(
        self,
        async_session_factory: async_sessionmaker[AsyncSession],
        fk_reflector: FkReflector,
        models_list: CombinableList,
    ):

        self.async_session_factory = async_session_factory
        self.fk_reflector = fk_reflector

        self.models_list = models_list

    @classmethod
    async def init(
        cls,
        async_session_factory: async_sessionmaker[AsyncSession],
        models_to_join: list[type[SQLALCHEMY_MODEL_TYPE]],
    ):
        refl = FkReflector(
            async_session_factory, [m.__tablename__ for m in models_to_join]
        )
        fks_reflection = await refl.get_fks_reflection()
        models_list = CombinableList(fks_reflection, models_to_join)
        return cls(async_session_factory, refl, models_list)

    async def _compile_select_stmt(
        self,
        base_model: type[SQLALCHEMY_MODEL_TYPE],
        selectable: Iterable[InstrumentedAttribute | type[SQLALCHEMY_MODEL_TYPE]],
        *where_clasue,
    ) -> Select:
        stmt = Select(*selectable).select_from(self.models_list[0])
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
        stmt = stmt.join(
            base_model,
            await self.fk_reflector.get_field_to_which_connect(
                self.models_list[0], base_model.__tablename__
            )
            == getattr(base_model, "uuididf"),
        )
        from ws.db.models import Items, Roles

        Roles.users

        stmt = stmt.options(joinedload(Items.type))
        if where_clasue is not None:
            stmt = stmt.where(*where_clasue)
        return stmt

    async def _create_filters(
        self, model: type[SQLALCHEMY_MODEL_TYPE], **kwargs
    ) -> list:
        if len(kwargs.items()) == 0:
            raise ValueError("Expected at least on keyword argument")
        filters = []
        for k, v in kwargs.items():
            try:
                filters.append(getattr(model, k) == v)
            except AttributeError:
                raise AttributeError(
                    f"Model {model.__name__} doesn't have how field '{k}'"
                )
        return filters

    async def _execute_stmt(self, stmt):
        async with self.async_session_factory() as session:
            return await session.execute(stmt)

    async def find(
        self,
        base_model: type[SQLALCHEMY_MODEL_TYPE],
        selectable: Iterable[InstrumentedAttribute | type[SQLALCHEMY_MODEL_TYPE]],
        **kwargs,
    ) -> list:
        filters = await self._create_filters(base_model, **kwargs)
        stmt = await self._compile_select_stmt(base_model, selectable, *filters)
        print(f"\n\n\n\n\n STMT {stmt} \n\n\n\n")

        result = await self._execute_stmt(stmt)
        return result.scalars().all()
