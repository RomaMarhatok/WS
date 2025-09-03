import uuid
from functools import lru_cache
from typing import Generic, get_args, Type
from sqlalchemy import update, Select, inspect, Inspector
from sqlalchemy.exc import IntegrityError
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from asyncpg.exceptions import ForeignKeyViolationError, UniqueViolationError
from abc import ABC
from ws.db.types import SQLALCHEMY_MODEL_TYPE, PYDANTIC_SCHEMA_TYPE
from ws.db.exceptions import (
    EntityNotFoundException,
    CouldNotCreateEntityException,
    ForeignKeyNotExist,
    EntityAlreadyExistException,
)
from ws.db.models import BaseModel


class LinkedTable:
    def __init__(
        self,
        linked_table_model: Type[SQLALCHEMY_MODEL_TYPE],
        constrained_column_name: str,
        referred_column_name: str,
    ):
        self.linked_table_model = linked_table_model
        self.constrained_column_name = constrained_column_name
        self.referred_column_name = referred_column_name

    def get_orm_filed(self):
        return getattr(self.linked_table_model, self.referred_column_name)

    def __repr__(self):
        return f"Linked table for {self.linked_table_model} model"


class Reflection:
    def __init__(
        self,
        reflected_table_model: Type[SQLALCHEMY_MODEL_TYPE],
        linked_tables: list[LinkedTable],
    ):
        self.reflected_table_model = reflected_table_model
        self.linked_tables = linked_tables

    def __contains__(self, item: Type[SQLALCHEMY_MODEL_TYPE]) -> bool:
        for t in self.linked_tables:
            if t.linked_table_model == item:
                return True
        return False

    async def get_linked_table_models(self) -> set[Type[SQLALCHEMY_MODEL_TYPE]]:
        return set(
            [linked_table.linked_table_model for linked_table in self.linked_tables]
        )

    async def get_linked_table(self, tablename: str) -> LinkedTable:
        for linked_table in self.linked_tables:
            if linked_table.linked_table_model.__tablename__ == tablename:
                return linked_table

    async def get_orm_constrained_filed(self, tablename: str):
        linked_table = await self.get_linked_table(tablename)
        return getattr(self.reflected_table_model, linked_table.constrained_column_name)


class GenericRepository(Generic[SQLALCHEMY_MODEL_TYPE], ABC):

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self.model = self._get_entity_classes()
        self.session_factory = session_factory

    async def save(self, dto: PYDANTIC_SCHEMA_TYPE) -> SQLALCHEMY_MODEL_TYPE:
        async with self.session_factory() as session:
            try:
                entity = self.model(**dto.model_dump())
                session.add(entity)
                await session.commit()
                await session.refresh(entity)
                return entity
            except IntegrityError as exc:
                await session.rollback()
                error_msg: str = exc.args[0]
                if "DETAIL" in error_msg:
                    error_msg = error_msg[error_msg.find("DETAIL") :]
                if isinstance(exc.orig.__cause__, ForeignKeyViolationError):
                    raise ForeignKeyNotExist(error_msg)
                if isinstance(exc.orig.__cause__, UniqueViolationError):
                    raise EntityAlreadyExistException(error_msg)
                raise CouldNotCreateEntityException from exc

    async def update(self, dto: PYDANTIC_SCHEMA_TYPE) -> SQLALCHEMY_MODEL_TYPE:
        async with self.session_factory() as session:
            try:
                stmt = (
                    update(self.model)
                    .where(self.model.uuididf == dto.uuididf)
                    .values(**dto.model_dump())
                    .returning(self.model)
                )
                entity = (await session.execute(stmt)).scalar_one_or_none()
            except IntegrityError as exc:
                await session.rollback()
                error_msg: str = exc.args[0]
                if "DETAIL" in error_msg:
                    error_msg = error_msg[error_msg.find("DETAIL") :]
                if isinstance(exc.orig.__cause__, ForeignKeyViolationError):
                    raise ForeignKeyNotExist(error_msg)
            if entity is None:
                raise EntityNotFoundException(
                    f"Entity {self.model.__name__} with UUID {dto.uuididf} not found"
                )
            await session.commit()
            return entity

    async def delete(self, uuididf: uuid.UUID) -> None:
        async with self.session_factory() as session:
            q = Select(self.model).where(self.model.uuididf == uuididf)
            entity = (await session.execute(q)).scalar_one_or_none()
            if entity is None:
                raise EntityNotFoundException(
                    f"Entity {self.model.__name__} with UUID {uuididf} not found"
                )
            await session.delete(entity)
            await session.commit()

    async def get_batch(
        self, limit: int = 10, offset: int = 0
    ) -> list[SQLALCHEMY_MODEL_TYPE]:
        async with self.session_factory() as session:
            stmt = Select(self.model).limit(limit).offset(offset)
            return (await session.execute(stmt)).scalars().all()

    async def _create_filters(self, **kwargs) -> list:
        if len(kwargs.items()) == 0:
            raise ValueError("Expected at least on keyword argument")
        filters = []
        for k, v in kwargs.items():
            try:
                filters.append(getattr(self.model, k) == v)
            except AttributeError:
                raise AttributeError(
                    f"Model {self.model.__name__} doesn't have how field '{k}'"
                )
        return filters

    async def get(self, **kwargs) -> SQLALCHEMY_MODEL_TYPE:
        filters = await self._create_filters(**kwargs)
        async with self.session_factory() as session:
            stmt = Select(self.model).where(*filters)
            entity = (await session.execute(stmt)).scalar_one_or_none()
            if entity is None:
                raise EntityNotFoundException(
                    f"Entity {self.model.__name__}"
                    + f" with values {filters} not found"
                )
            return entity

    async def _swap_inner_join(
        self,
        stmt: Select,
        the_attached_table: Type[SQLALCHEMY_MODEL_TYPE],
        the_table_to_which_is_attached: Type[SQLALCHEMY_MODEL_TYPE],
        union_table_reflection: Reflection,
        get_table_name_from_attached_table: bool = False,
    ) -> Select:
        tablename_for_getting_fields = (
            the_table_to_which_is_attached.__tablename__
            if not get_table_name_from_attached_table
            else the_attached_table.__tablename__
        )
        return stmt.join(
            the_attached_table,
            await union_table_reflection.get_orm_constrained_filed(
                tablename_for_getting_fields
            )
            == (
                await union_table_reflection.get_linked_table(
                    tablename_for_getting_fields
                )
            ).get_orm_filed(),
        )

    async def get_with_join(
        self,
        joined_tables: list[Type[SQLALCHEMY_MODEL_TYPE]],
        exclude: list[Type[SQLALCHEMY_MODEL_TYPE]] = None,
    ):
        joined_tables.insert(0, self.model)
        fks_reflection = await self._get_foreign_keys_reflection()
        reflections = [
            fk_ref
            for fk_ref in fks_reflection
            if len(
                (await fk_ref.get_linked_table_models()).intersection(
                    set(joined_tables)
                )
            )
            >= 2
        ]
        reflections = [r for r in reflections if r.reflected_table_model not in exclude]

        stmt = Select(joined_tables[0])
        already_attched_table_list = set()
        already_attched_union_table = set()
        for bearing_table in joined_tables:
            if len(already_attched_table_list) == len(set(joined_tables)):
                break
            for reflection in reflections:
                if (
                    bearing_table in reflection
                    and reflection not in already_attched_union_table
                ):
                    stmt = await self._swap_inner_join(
                        stmt,
                        reflection.reflected_table_model,
                        bearing_table,
                        reflection,
                    )

                    already_attched_table_list.add(bearing_table)
                    intersection_of_linked_tables = (
                        set(joined_tables).difference(already_attched_table_list)
                    ).intersection(await reflection.get_linked_table_models())
                    if len(intersection_of_linked_tables) != 0:
                        for t in intersection_of_linked_tables:
                            stmt = await self._swap_inner_join(
                                stmt,
                                t,
                                reflection.reflected_table_model,
                                reflection,
                                get_table_name_from_attached_table=True,
                            )
                            already_attched_table_list.add(t)
                    already_attched_union_table.add(reflection)

        return stmt

    async def find(self, **kwargs) -> list[SQLALCHEMY_MODEL_TYPE]:
        filters = await self._create_filters(**kwargs)
        async with self.session_factory() as session:
            stmt = Select(self.model).where(*filters)
            entities = (await session.execute(stmt)).scalars().all()
            return entities

    @classmethod
    @lru_cache(maxsize=1)
    def _get_entity_classes(cls) -> Type[SQLALCHEMY_MODEL_TYPE]:
        generic_types_of_repo = getattr(cls, "__orig_bases__")[0]
        sqlachemy_entity_class = get_args(generic_types_of_repo)[0]
        return sqlachemy_entity_class

    @lru_cache(maxsize=1)
    async def _get_foreign_keys_reflection(
        self,
    ) -> list[Reflection]:
        async with self.session_factory() as session:

            def _get_fk_reflection_from_db(sync_conn: Connection):
                inspector: Inspector = inspect(sync_conn)
                return inspector.get_multi_foreign_keys()

            _reflected_foreign_keys = None
            async with session.bind.connect() as conn:
                _reflected_foreign_keys = await conn.run_sync(
                    _get_fk_reflection_from_db
                )
            reflection: list[Reflection] = []
            for (
                _,
                tablename,
            ), table_fks_reflection_list in _reflected_foreign_keys.items():

                if len(table_fks_reflection_list) == 0:
                    continue
                reflected_table = None
                _mentioned_tables = []
                for fk_reflection_data in table_fks_reflection_list:
                    linked_table = LinkedTable(
                        linked_table_model=(
                            await self._get_table_class_from_name(
                                fk_reflection_data["referred_table"]
                            )
                        ),
                        referred_column_name=fk_reflection_data["referred_columns"][0],
                        constrained_column_name=fk_reflection_data[
                            "constrained_columns"
                        ][0],
                    )
                    _mentioned_tables.append(linked_table)
                    if reflected_table is None:
                        reflected_table = Reflection(
                            reflected_table_model=await self._get_table_class_from_name(
                                tablename
                            ),
                            linked_tables=_mentioned_tables,
                        )
                    reflected_table.linked_tables.append(linked_table)
                reflection.append(reflected_table)

            return reflection

    async def _get_table_class_from_name(
        self, tablename: str
    ) -> Type[SQLALCHEMY_MODEL_TYPE]:
        if issubclass(self.model.__base__, BaseModel):
            for table in self.model.__base__.__subclasses__():
                if table.__tablename__ == tablename:
                    return table
            raise AttributeError(f"The table {tablename} doesn't exist")
