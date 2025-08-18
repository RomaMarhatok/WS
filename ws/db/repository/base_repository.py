import uuid
from abc import ABC
from typing import Generic
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from asyncpg.exceptions import ForeignKeyViolationError, UniqueViolationError
from ws.db.types import SQLALCHEMY_MODEL_TYPE, PYDANTIC_SCHEMA_TYPE

from ws.db.session import get_session_factory
from ws.db.exceptions import (
    EntityNotFoundException,
    CouldNotCreateEntityException,
    ForeignKeyNotExist,
    EntityAlreadyExistException,
)


class GenericRepository(ABC, Generic[SQLALCHEMY_MODEL_TYPE, PYDANTIC_SCHEMA_TYPE]):

    def __init__(self):
        self.session_factory = get_session_factory()

    @property
    def _model(self) -> SQLALCHEMY_MODEL_TYPE:
        raise NotImplementedError

    async def save(self, dto: PYDANTIC_SCHEMA_TYPE) -> SQLALCHEMY_MODEL_TYPE:
        async with self.session_factory() as session:
            try:
                entity = self._model(**dto.model_dump())
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

    async def get_by_uuididf(self, uuididf: uuid.UUID) -> SQLALCHEMY_MODEL_TYPE:
        async with self.session_factory() as session:
            q = select(self._model).where(self._model.uuididf == uuididf)
            entity = (await session.execute(q)).scalar_one_or_none()
            if entity is None:
                raise EntityNotFoundException(
                    f"Entity {self._model.__name__} with UUID {uuididf} not found"
                )
            return entity

    async def update(self, dto: PYDANTIC_SCHEMA_TYPE) -> SQLALCHEMY_MODEL_TYPE:
        async with self.session_factory() as session:
            stmt = (
                update(self._model)
                .where(self._model.uuididf == dto.uuididf)
                .values(**dto.model_dump())
                .returning(self._model)
            )
            entity = (await session.execute(stmt)).scalar_one_or_none()

            if entity is None:
                raise EntityNotFoundException(
                    f"Entity {self._model.__name__} with UUID {dto.uuididf} not found"
                )
            await session.commit()
            return entity

    async def delete(self, uuididf: uuid.UUID) -> None:
        async with self.session_factory() as session:
            q = select(self._model).where(self._model.uuididf == uuididf)
            entity = (await session.execute(q)).scalar_one_or_none()
            if entity is None:
                raise EntityNotFoundException(
                    f"Entity {self._model.__name__} with UUID {uuididf} not found"
                )
            await session.delete(entity)
            await session.commit()

    async def get_batch(self) -> list[SQLALCHEMY_MODEL_TYPE]:
        async with self.session_factory() as session:
            return (await session.execute(select(self._model))).scalars().all()
