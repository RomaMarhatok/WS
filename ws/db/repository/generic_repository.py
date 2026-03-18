from abc import ABC
from typing import Generic, TypeVar, Sequence, get_args

from pydantic import BaseModel as PydanticBaseModel

from sqlalchemy import Update, Select, Delete, Insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from asyncpg.exceptions import (
    ForeignKeyViolationError,
    UniqueViolationError,
    RestrictViolationError,
)

from ws.db.models import BaseModel
from ws.api.v1.routers.exceptions import (
    NotFoundError,
    UniqueError,
    DatabaseError,
    ConflictError,
)

SQLALCHEMY_MODEL_TYPE = TypeVar("SQLALCHEMY_MODEL_TYPE", bound=BaseModel)
type CREATE_SCHEMA = PydanticBaseModel
type UPDATE_SCHEMA = PydanticBaseModel


class GenericRepository(Generic[SQLALCHEMY_MODEL_TYPE], ABC):
    model: type[SQLALCHEMY_MODEL_TYPE]

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance.model = get_args(cls.__orig_bases__[0])[0]
        return instance

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        dto: CREATE_SCHEMA,
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

    async def update(self, _id: int, dto: UPDATE_SCHEMA) -> SQLALCHEMY_MODEL_TYPE:
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

    async def delete(self, _id: int) -> None:
        try:
            stmt = Delete(self.model).where(self.model.id == _id)
            result = await self.db.execute(stmt)
            if result.rowcount != 1:
                raise NotFoundError(
                    message=f"Запись {self.model.__tablename__} c id {_id} не была удалена !"
                )
            await self.db.flush()
        except IntegrityError as e:
            match e.orig.sqlstate:
                case RestrictViolationError.sqlstate:
                    raise ConflictError(
                        f"Запись {self.model.__tablename__} c id {_id} является внешним ключем с политикой RESTRICT !"
                    )
                case _:
                    raise DatabaseError(
                        message=str(e.orig),
                    ) from e

    async def get_batch(
        self, limit: int = None, offset: int = None
    ) -> Sequence[SQLALCHEMY_MODEL_TYPE]:
        stmt = Select(self.model).limit(limit).offset(offset)
        if limit:
            stmt = stmt.limit(limit)
        if offset:
            stmt = stmt.offset(offset)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get(self, _id: int) -> SQLALCHEMY_MODEL_TYPE:
        stmt = Select(self.model).where(self.model.id == _id)
        result = await self.db.execute(stmt)
        obj_from_db = result.scalars().first()
        if obj_from_db is None:
            raise NotFoundError(
                message=f"Запись {self.model.__tablename__} c id {_id} не найдена !"
            )
        return obj_from_db

    async def get_by_column(self, **kwargs) -> SQLALCHEMY_MODEL_TYPE:
        if not kwargs:
            raise ValueError(
                "Вы должны предоставить хотя бы одно поле для фильтрации !"
            )
        for passed_fields in kwargs.keys():
            if passed_fields not in self.model.__table__.columns.keys():
                raise ValueError(
                    f"В таблице {self.model.__tablename__} не существует поля {passed_fields}!"
                )

        stmt = Select(self.model).filter_by(**kwargs)
        result = await self.db.execute(stmt)
        obj_from_db = result.scalars().first()
        if obj_from_db is None:
            raise NotFoundError(
                message=f"Запись {self.model.__tablename__} c полями {kwargs.keys()} и"
                "значениями {kwargs.values()} не найдена !",
            )
        return obj_from_db
