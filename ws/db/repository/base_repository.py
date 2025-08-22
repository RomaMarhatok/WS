import uuid
from abc import ABC
from functools import lru_cache
from typing import Generic, get_args
from sqlalchemy import select, update, Select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from asyncpg.exceptions import ForeignKeyViolationError, UniqueViolationError
from ws.db.types import SQLALCHEMY_MODEL_TYPE, PYDANTIC_SCHEMA_TYPE
from ws.db.exceptions import (
    EntityNotFoundException,
    CouldNotCreateEntityException,
    ForeignKeyNotExist,
    EntityAlreadyExistException,
)


class GenericRepository(ABC, Generic[SQLALCHEMY_MODEL_TYPE, PYDANTIC_SCHEMA_TYPE]):

    def __init__(self, session: AsyncSession):
        self._model, self._dto = self._get_entity_classes()
        self.session = session

    async def save(self, dto: PYDANTIC_SCHEMA_TYPE) -> SQLALCHEMY_MODEL_TYPE:
        async with self.session:
            try:
                entity = self._model(**dto.model_dump())
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

    async def get_by_uuididf(self, uuididf: uuid.UUID) -> SQLALCHEMY_MODEL_TYPE:
        async with self.session:
            q = Select(self._model).where(self._model.uuididf == uuididf)
            entity = (await self.session.execute(q)).scalar_one_or_none()
            if entity is None:
                raise EntityNotFoundException(
                    f"Entity {self._model.__name__} with UUID {uuididf} not found"
                )
            return entity

    async def update(self, dto: PYDANTIC_SCHEMA_TYPE) -> SQLALCHEMY_MODEL_TYPE:
        async with self.session:
            try:
                stmt = (
                    update(self._model)
                    .where(self._model.uuididf == dto.uuididf)
                    .values(**dto.model_dump())
                    .returning(self._model)
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
                    f"Entity {self._model.__name__} with UUID {dto.uuididf} not found"
                )
            await self.session.commit()
            return entity

    async def delete(self, uuididf: uuid.UUID) -> None:
        async with self.session:
            q = Select(self._model).where(self._model.uuididf == uuididf)
            entity = (await self.session.execute(q)).scalar_one_or_none()
            if entity is None:
                raise EntityNotFoundException(
                    f"Entity {self._model.__name__} with UUID {uuididf} not found"
                )
            await self.session.delete(entity)
            await self.session.commit()

    async def get_batch(self) -> list[SQLALCHEMY_MODEL_TYPE]:
        async with self.session:
            return (await self.session.execute(select(self._model))).scalars().all()

    async def get_by_name(self, name: str, name_field=None) -> SQLALCHEMY_MODEL_TYPE:
        entity_name_field = (
            name_field if name_field is not None else self._get_entity_name_field()
        )
        async with self.session:
            stmt = Select(self._model).where(entity_name_field == name)
            entity = (await self.session.execute(stmt)).scalar_one_or_none()
            if entity is None:
                raise EntityNotFoundException(
                    f"Entity {self._model.__name__} with name {name} not found"
                )
            return entity

    @classmethod
    @lru_cache(maxsize=1)
    def _get_entity_classes(cls) -> tuple[SQLALCHEMY_MODEL_TYPE, PYDANTIC_SCHEMA_TYPE]:
        generic_types_of_repo = getattr(cls, "__orig_bases__")[0]
        sqlachemy_entity_class, pydantic_entity_class = get_args(generic_types_of_repo)
        return sqlachemy_entity_class, pydantic_entity_class

    def _get_entity_name_field(self):
        # find all fields wich contain word name
        name_fields = list(
            filter(lambda x: "__" not in x and "name" in x, dir(self._model))
        )
        if len(name_fields) == 0:
            raise ValueError(
                f"Entity {self._model} doesn't have field wich contain word 'name' "
            )
        return getattr(self._model, name_fields[0])
