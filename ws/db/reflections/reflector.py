from functools import lru_cache
from typing import Type
from sqlalchemy.engine import Engine, Connection
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy import inspect
from sqlalchemy.orm import DeclarativeBase
from ws.db.types import SQLALCHEMY_MODEL_TYPE
from sqlalchemy.engine.interfaces import ReflectedForeignKeyConstraint


class LinkedTable:
    def __init__(
        self,
        linked_orm_model: Type[SQLALCHEMY_MODEL_TYPE],
        referred_column_name: str,
    ):
        self.linked_orm_model = linked_orm_model
        self.referred_column_name = referred_column_name

    def get_orm_referred_column_filed(self):
        """Return result of 'getattr' for referred_column_name of linked_orm_model"""
        return getattr(self.linked_orm_model, self.referred_column_name)

    def __repr__(self):
        return f"Linked table for {self.linked_orm_model} model"


class UnionTable:
    def __init__(
        self,
        union_orm_model: Type[SQLALCHEMY_MODEL_TYPE],
        linked_tables: list[LinkedTable],
        constrained_fields_map: dict[str, str],
    ):
        self.union_orm_model = union_orm_model
        self.linked_tables = linked_tables
        self.constrained_fields_map = constrained_fields_map

    def __contains__(self, item: Type[SQLALCHEMY_MODEL_TYPE]) -> bool:
        for t in self.linked_tables:
            if t.linked_orm_model == item:
                return True
        return False

    async def get_linked_table_models(self) -> set[Type[SQLALCHEMY_MODEL_TYPE]]:
        return set(
            [linked_table.linked_orm_model for linked_table in self.linked_tables]
        )

    async def get_linked_table(self, tablename: str) -> LinkedTable:
        for linked_table in self.linked_tables:
            if linked_table.linked_orm_model.__tablename__ == tablename:
                return linked_table

    async def get_orm_constrained_filed(self, tablename: str):
        column_field = self.constrained_fields_map.get(tablename)
        if column_field is None:
            raise AttributeError(f"{self.union_orm_model} doesn'thave constrained fiel")
        return getattr(self.union_orm_model, self.constrained_fields_map[tablename])


class JoinReflector:
    def __init__(self, engine: Engine | AsyncEngine, base_model: DeclarativeBase):
        self.engine = engine
        self.base_model = base_model

    @lru_cache(maxsize=1)
    def get_all_models_from(self) -> list[Type[SQLALCHEMY_MODEL_TYPE]]:
        if issubclass(self.base_model, DeclarativeBase):
            return self.base_model.__subclasses__()
        raise AttributeError(
            f"The {self.base_model} must be a subclass of 'DeclarativeBase'"
        )

    async def _get_orm_model(self, tablename: str):
        for model in self.get_all_models_from():
            if model.__tablename__ == tablename:
                return model
        raise AttributeError("This table doesn't exist")

    async def _get_fks_reflect_of_table(
        self, table_reflection: ReflectedForeignKeyConstraint
    ) -> LinkedTable:
        linked_model = await self._get_orm_model(table_reflection["referred_table"])
        referred_column_name = table_reflection["referred_columns"][0]
        linked_table = LinkedTable(
            linked_orm_model=linked_model,
            referred_column_name=referred_column_name,
        )
        return linked_table

    @lru_cache(maxsize=1)
    async def get_foreign_keys_reflection(
        self,
    ) -> list[UnionTable]:
        async with self.engine.connect() as conn:

            def _get_fk_reflection_from_db(sync_conn: Connection):
                inspector = inspect(sync_conn)
                return inspector.get_multi_foreign_keys()

            _reflected_foreign_keys = await conn.run_sync(_get_fk_reflection_from_db)
            reflection_of_union_tables: list[UnionTable] = []
            for (
                _,
                tablename,
            ), table_fks_reflection_list in _reflected_foreign_keys.items():

                if len(table_fks_reflection_list) == 0:
                    continue
                reflected_table = None
                linked_tables = []
                constrained_fields_map = dict()
                for fk_reflection_data in table_fks_reflection_list:
                    linked_table = await self._get_fks_reflect_of_table(
                        fk_reflection_data
                    )
                    linked_tables.append(linked_table)
                    constrained_fields_map.update(
                        {
                            fk_reflection_data["referred_table"]: fk_reflection_data[
                                "constrained_columns"
                            ][0]
                        }
                    )
                    if reflected_table is None:
                        reflected_table = UnionTable(
                            union_orm_model=await self._get_orm_model(tablename),
                            linked_tables=linked_tables,
                            constrained_fields_map=constrained_fields_map,
                        )
                    reflected_table.linked_tables.append(linked_table)
                reflection_of_union_tables.append(reflected_table)
            return reflection_of_union_tables
