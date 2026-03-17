from abc import ABC
from typing import Generic, TypeVar, Sequence

from pydantic import BaseModel as PydanticBaseModel

from sqlalchemy import Update, Select, Delete, Insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from asyncpg.exceptions import ForeignKeyViolationError, UniqueViolationError

from ws.db.models import BaseModel
from ws.api.v1.routers.exceptions import NotFoundError, UniqueError, DatabaseError

SQLALCHEMY_MODEL_TYPE = TypeVar("SQLALCHEMY_MODEL_TYPE", bound=BaseModel)
CREATE_SCHEMA_TYPE = TypeVar("CREATE_SCHEMA_TYPE", bound=PydanticBaseModel)
UPDATE_SCHEMA_TYPE = TypeVar("UPDATE_SCHEMA_TYPE", bound=PydanticBaseModel)


class GenericRepository(
    Generic[SQLALCHEMY_MODEL_TYPE, CREATE_SCHEMA_TYPE, UPDATE_SCHEMA_TYPE], ABC
):
    model: SQLALCHEMY_MODEL_TYPE

    def __new__(cls):
        instance = super().__new__()
        instance.model = getattr(cls, "__orig_bases__")[0][0]
        return instance

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        dto: CREATE_SCHEMA_TYPE,
        exclude: list[str] = None,
        by_alias: bool = False,
    ) -> SQLALCHEMY_MODEL_TYPE:
        try:
            stmt = Insert(self.model).values(
                **dto.model_dump(exclude=exclude, exclude_none=True, by_alias=by_alias)
            )
            result = await self.db.execute(stmt)
            await self.db.flush()
            refresh_obj = await self.get(result.inserted_primary_key[0])
            return refresh_obj
        except IntegrityError as e:
            match e.orig.sqlstate:
                case UniqueViolationError.sqlstate:
                    raise UniqueError(model_name=self.model.__name__) from e
                case ForeignKeyViolationError.sqlstate:
                    raise NotFoundError(
                        message="Вы пытаетесь связать поля c несуществующими "
                        "значениями FK!",
                    ) from e
                case _:
                    raise DatabaseError(
                        message=str(e),
                    ) from e

    async def update(self, _id: int, dto: UPDATE_SCHEMA_TYPE) -> SQLALCHEMY_MODEL_TYPE:
        try:
            stmt = (
                Update(self.model)
                .where(self.model.id == _id)
                .values(**dto.model_dump())
                .returning(self.model)
            )
            result = await self.db.execute(stmt)
            await self.db.flush()
            return result.scalars().first()
        except IntegrityError as e:
            match e.orig.sqlstate:
                case UniqueViolationError.sqlstate:
                    raise UniqueError(model_name=self.model.__name__) from e
                case ForeignKeyViolationError.sqlstate:
                    raise NotFoundError(
                        message="Вы пытаетесь связать поля c несуществующими "
                        "значениями FK!",
                    ) from e
                case _:
                    raise DatabaseError(
                        message=str(e.orig),
                    ) from e

    async def delete(self, _id: int):
        stmt = Delete(self.model).where(self.model.id == _id)
        result = await self.db.execute(stmt)
        if result.rowcount != 1:
            raise NotFoundError(
                message=f"Запись {self.model.__tablename__} c uuididf {_id} не была удалена !"
            )
        await self.db.flush()

    async def get_batch(
        self, limit: int = 10, offset: int = 0
    ) -> Sequence[SQLALCHEMY_MODEL_TYPE]:
        stmt = Select(self.model).limit(limit).offset(offset)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get(self, _id: int, exclude: list[str] = None) -> SQLALCHEMY_MODEL_TYPE:
        stmt = Select(self.model.group_by_fields(exclude=exclude)).where(
            self.model.id == _id
        )
        result = await self.db.execute(stmt)
        obj_from_db = result.scalars().first()
        if obj_from_db is None:
            raise NotFoundError(
                message=f"Запись {self.model.__tablename__} c uuididf {_id} не найдена!"
            )
        return obj_from_db
