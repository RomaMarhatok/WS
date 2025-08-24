import uuid
from functools import lru_cache
from typing import Generic, get_args
from sqlalchemy import select, update, Select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
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

    def __init__(self, session: AsyncSession):
        self.model = self._get_entity_classes()
        self.session = session

    async def save(self, dto: PYDANTIC_SCHEMA_TYPE) -> SQLALCHEMY_MODEL_TYPE:
        async with self.session:
            try:
                entity = self.model(**dto.model_dump())
                self.session.add(entity)
                await self.session.commit()
                await self.session.refresh(entity)
                return entity
            except IntegrityError as exc:
                await self.session.rollback()
                error_msg: str = exc.args[0]
                if "DETAIL" in error_msg:
                    error_msg = error_msg[error_msg.find("DETAIL") :]
                if isinstance(exc.orig.__cause__, ForeignKeyViolationError):
                    raise ForeignKeyNotExist(error_msg)
                if isinstance(exc.orig.__cause__, UniqueViolationError):
                    raise EntityAlreadyExistException(error_msg)
                raise CouldNotCreateEntityException from exc

    async def update(self, dto: PYDANTIC_SCHEMA_TYPE) -> SQLALCHEMY_MODEL_TYPE:
        async with self.session:
            try:
                stmt = (
                    update(self.model)
                    .where(self.model.uuididf == dto.uuididf)
                    .values(**dto.model_dump())
                    .returning(self.model)
                )
                entity = (await self.session.execute(stmt)).scalar_one_or_none()
            except IntegrityError as exc:
                await self.session.rollback()
                error_msg: str = exc.args[0]
                if "DETAIL" in error_msg:
                    error_msg = error_msg[error_msg.find("DETAIL") :]
                if isinstance(exc.orig.__cause__, ForeignKeyViolationError):
                    raise ForeignKeyNotExist(error_msg)
            if entity is None:
                raise EntityNotFoundException(
                    f"Entity {self.model.__name__} with UUID {dto.uuididf} not found"
                )
            await self.session.commit()
            return entity

    async def delete(self, uuididf: uuid.UUID) -> None:
        async with self.session:
            q = Select(self.model).where(self.model.uuididf == uuididf)
            entity = (await self.session.execute(q)).scalar_one_or_none()
            if entity is None:
                raise EntityNotFoundException(
                    f"Entity {self.model.__name__} with UUID {uuididf} not found"
                )
            await self.session.delete(entity)
            await self.session.commit()

    async def get_batch(self) -> list[SQLALCHEMY_MODEL_TYPE]:
        async with self.session:
            return (await self.session.execute(select(self.model))).scalars().all()

    async def get(self, **kwargs) -> SQLALCHEMY_MODEL_TYPE:
        if len(kwargs.items()) != 1:
            raise ValueError(f"Method {self.get.__name__} accept only one argument")
        field, value = list(kwargs.items())[0]
        try:
            async with self.session:
                model_field = getattr(self.model, field)
                stmt = Select(self.model).where(model_field == value)
                entity = (await self.session.execute(stmt)).scalar_one_or_none()
                if entity is None:
                    raise EntityNotFoundException(
                        f"Entity {self.model.__name__}"
                        + f" with {model_field} == {value} not found"
                    )
                return entity
        except AttributeError:
            raise AttributeError(
                f"Model {self.model.__name__} doesn't have {field} field"
            )

    @classmethod
    @lru_cache(maxsize=1)
    def _get_entity_classes(cls) -> SQLALCHEMY_MODEL_TYPE:
        generic_types_of_repo = getattr(cls, "__orig_bases__")[0]
        sqlachemy_entity_class = get_args(generic_types_of_repo)[0]
        return sqlachemy_entity_class
