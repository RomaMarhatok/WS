import uuid
from abc import ABC
from functools import lru_cache
from typing import Generic, get_args, Type
from sqlalchemy import Update, Select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import ColumnExpressionArgument
from asyncpg.exceptions import ForeignKeyViolationError, UniqueViolationError
from ws.db.repository.exceptions import (
    EntityNotFoundException,
    CouldNotCreateEntityException,
    ForeignKeyNotExist,
    EntityAlreadyExistException,
)
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from ws.db.types import SQLALCHEMY_MODEL_TYPE, PYDANTIC_SCHEMA_TYPE


class GenericRepository(Generic[SQLALCHEMY_MODEL_TYPE], ABC):

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
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
                    Update(self.model)
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
        self, limit: int = 10, offset: int = 0
    ) -> list[SQLALCHEMY_MODEL_TYPE]:
        async with self.session_factory() as session:
            stmt = Select(self.model).limit(limit).offset(offset)
            return (await session.execute(stmt)).scalars().all()

    async def get(self, uuididf: uuid.UUID) -> SQLALCHEMY_MODEL_TYPE:
        async with self.session_factory() as session:
            stmt = Select(self.model).where(self.model.uuididf == uuididf)
            entity = (await session.execute(stmt)).scalar_one_or_none()
            if entity is None:
                raise EntityNotFoundException(
                    f"Entity {self.model.__name__} with UUID {uuididf} not found"
                )
            return entity

    async def find(
        self,
        *filters: ColumnExpressionArgument[bool],
        get_first: bool = False,
    ) -> list[SQLALCHEMY_MODEL_TYPE] | SQLALCHEMY_MODEL_TYPE:
        async with self.session_factory() as session:
            stmt = Select(self.model).where(*filters)
            entities = (await session.execute(stmt)).scalars()
            if get_first:
                return entities.first()
            return entities.all()

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
        if type(exc.orig.__cause__) not in integrity_error_map:
            raise CouldNotCreateEntityException from exc
        raise integrity_error_map[type(exc.orig.__cause__)](error_msg) from exc
