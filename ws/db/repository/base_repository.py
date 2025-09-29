import uuid
from abc import ABC
from functools import lru_cache
from typing import Generic, get_args, Type, Iterable, Self
from sqlalchemy import update, Select
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError
from asyncpg.exceptions import ForeignKeyViolationError, UniqueViolationError
from ws.db.repository.exceptions import (
    EntityNotFoundException,
    CouldNotCreateEntityException,
    ForeignKeyNotExist,
    EntityAlreadyExistException,
)
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from ws.db.types import SQLALCHEMY_MODEL_TYPE, PYDANTIC_SCHEMA_TYPE
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.orm.attributes import InstrumentedAttribute


class GenericRepository(Generic[SQLALCHEMY_MODEL_TYPE], ABC):

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self._stmt = None
        self.model = self._get_entity_class()
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
                self._exception_handler(exc)

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
                self._exception_handler(exc)
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
        self,
    ) -> list[SQLALCHEMY_MODEL_TYPE]:
        async with self.session_factory() as session:
            stmt = Select(self.model)
            return (await session.execute(stmt)).scalars()

    async def _create_where_condition(self, **kwargs) -> list:
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

    async def get(
        self,
        selectable: Iterable[InstrumentedAttribute | list[type[SQLALCHEMY_MODEL_TYPE]]],
        where_conditions: dict,
        passing_relation: list[RelationshipProperty] = None,
    ) -> SQLALCHEMY_MODEL_TYPE:
        conditions = await self._create_where_condition(**where_conditions)
        stmt = await self._get(
            selectable, where_conditions=conditions, passing_relation=passing_relation
        )
        async with self.session_factory() as session:
            entity = (await session.execute(stmt)).scalar_one_or_none()
            if entity is None:
                raise EntityNotFoundException(
                    f"Entity {self.model.__name__}"
                    + f" with values {",".join(f"({k} == {v})" for k, v in conditions.items())}"  # noqa
                    + "not found"
                )
            return entity

    async def search(self, searched_models, condition_pramas, attached_relationsips):
        pass

    async def find(self):
        pass

    async def by(self, **kwargs) -> Self:
        return self

    async def attach(self, relation: RelationshipProperty) -> Self:
        return self

    @classmethod
    @lru_cache(maxsize=1)
    def _get_entity_class(cls) -> Type[SQLALCHEMY_MODEL_TYPE]:
        generic_types_of_repo = getattr(cls, "__orig_bases__")[0]
        sqlachemy_entity_class = get_args(generic_types_of_repo)[0]
        return sqlachemy_entity_class

    def _exception_handler(self, exc: IntegrityError):
        error_msg: str = exc.args[0]
        if "DETAIL" in error_msg:
            error_msg = error_msg[error_msg.find("DETAIL") :]
        integrity_error_map = {
            ForeignKeyViolationError: ForeignKeyNotExist,
            UniqueViolationError: EntityAlreadyExistException,
        }
        if exc.orig.__cause__ not in integrity_error_map:
            raise CouldNotCreateEntityException from exc
        raise integrity_error_map[exc.orig.__cause__](error_msg) from exc

    async def _get(
        self,
        selectable: Iterable[InstrumentedAttribute | list[type[SQLALCHEMY_MODEL_TYPE]]],
        where_conditions: list = None,
        passing_relation: list[RelationshipProperty] = None,
    ) -> Select:
        stmt = Select(*selectable)
        if passing_relation is not None:
            stmt = stmt.options(*passing_relation)
        if where_conditions is not None:
            stmt = stmt.where(*where_conditions)
        return stmt
