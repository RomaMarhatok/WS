import uuid
from functools import lru_cache
from typing import Generic, get_args
from sqlalchemy import update, Select
from sqlalchemy.exc import IntegrityError
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

    async def find(self, **kwargs) -> list[SQLALCHEMY_MODEL_TYPE]:
        filters = await self._create_filters(**kwargs)
        async with self.session_factory() as session:
            stmt = Select(self.model).where(*filters)
            entities = (await session.execute(stmt)).scalars().all()
            return entities

    @classmethod
    @lru_cache(maxsize=1)
    def _get_entity_classes(cls) -> SQLALCHEMY_MODEL_TYPE:
        generic_types_of_repo = getattr(cls, "__orig_bases__")[0]
        sqlachemy_entity_class = get_args(generic_types_of_repo)[0]
        return sqlachemy_entity_class
