import uuid
from abc import ABC
from functools import lru_cache
from typing import Generic, get_args, Type, Any
from sqlalchemy import Update, Select, Delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import ColumnExpressionArgument
from asyncpg.exceptions import ForeignKeyViolationError, UniqueViolationError
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from ws.db.types import SQLALCHEMY_MODEL_TYPE, PYDANTIC_SCHEMA_TYPE
from ws.db.repository.exceptions import (
    EntityNotFoundException,
    CouldNotCreateEntityException,
    ForeignKeyNotExist,
    EntityAlreadyExistException,
    ForeignKeyRestrictException,
)


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

    async def delete(
        self, entity_or_uuididf: uuid.UUID | SQLALCHEMY_MODEL_TYPE
    ) -> bool:
        entity_uuididf = entity_or_uuididf
        async with self.session_factory() as session:
            if isinstance(entity_or_uuididf, self.model):
                entity_uuididf = entity_or_uuididf.uuididf
            q = (
                Delete(self.model)
                .where(self.model.uuididf == entity_uuididf)
                .returning(self.model.uuididf)
            )
            try:
                deleted_uuididf = (await session.execute(q)).scalar_one_or_none()
                if deleted_uuididf is None:
                    raise EntityNotFoundException(
                        f"Entity {self.model.__name__} with"
                        + f"UUID {entity_uuididf} not found"
                    )
            except IntegrityError as exc:
                if isinstance(exc.orig.__cause__, ForeignKeyViolationError):
                    raise ForeignKeyRestrictException(str(exc.orig))
            await session.commit()
            return deleted_uuididf is not None

    async def get_batch(
        self, limit: int = 10, offset: int = 0
    ) -> list[SQLALCHEMY_MODEL_TYPE]:
        async with self.session_factory() as session:
            stmt = Select(self.model).limit(limit).offset(offset)
            return (await session.execute(stmt)).scalars().all()

    async def get(
        self,
        uuididf: uuid.UUID,
        *selected_fields: InstrumentedAttribute,
    ) -> SQLALCHEMY_MODEL_TYPE | list[Any] | Any:
        async with self.session_factory() as session:
            stmt = (
                Select(self.model)
                if len(selected_fields) == 0
                else Select(*selected_fields)
            )
            stmt = stmt.where(self.model.uuididf == uuididf)
            result = await session.execute(stmt)
            if len(selected_fields) == 0:
                entity = result.scalar_one_or_none()
                if entity is None:
                    raise EntityNotFoundException(
                        f"Entity {self.model.__name__} with UUID {uuididf} not found"
                    )
                return entity
            else:
                return result.all() if len(selected_fields) > 1 else result.scalar()

    async def find(
        self,
        *filters: ColumnExpressionArgument[bool],
        selected_fields: tuple[InstrumentedAttribute] | InstrumentedAttribute = None,
        get_first: bool = False,
        get_flat_result: bool = False,
    ) -> list[SQLALCHEMY_MODEL_TYPE] | SQLALCHEMY_MODEL_TYPE | list[Any]:
        if selected_fields is None and get_flat_result:
            raise ValueError(
                "You can't call get_falt_reuslt without passing selected_fields argument"
            )
        async with self.session_factory() as session:
            stmt = (
                Select(self.model)
                if selected_fields is None
                else Select(*selected_fields)
            )
            stmt = stmt.where(*filters)
            result = await session.execute(stmt)

            if selected_fields is None:
                return result.scalars().first() if get_first else result.scalars().all()
            else:
                if get_first:
                    return result.first()
                if get_flat_result:
                    return [item for row in result for item in row]
                else:
                    return result.all()

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
