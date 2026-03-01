from uuid import UUID
from typing import Any
from sqlalchemy import Update, Delete, Select
from .base_repository import BaseRepository
from ws.enums.types import SchemasTypes
from dto.user import UserCreationDTO, UserGetDTO
from models.users import Users


class UserRepository(BaseRepository):

    @property
    def _model(self) -> Users:
        return Users

    async def save(self, creation_data: UserCreationDTO):
        async with self.session_factory() as session:
            async with session.begin():
                try:
                    entity = self.model(**creation_data.model_dump())
                    session.add(entity)
                    await session.commit()
                except Exception as exc:
                    await session.rollback()
                    raise exc
            await session.close()

    async def create(self, creation_data: UserCreationDTO) -> Users:
        async with self.session_factory() as session:
            async with session.begin():
                try:
                    entity = self.model(**creation_data.model_dump())
                    session.add(entity)
                    await session.commit()
                    await session.refresh(entity)
                    return entity
                except Exception as exc:
                    await session.rollback()
                    raise exc
            await session.close()

    def compare_selected_fields_with_model(self, selected_fields: list[str]) -> Select:
        orm_fields = []
        for field in selected_fields:
            if not hasattr(self._model, field):
                raise AttributeError(f"Users model doesn't have {field} field")
            else:
                orm_fields.append(field)
        return Select(*orm_fields)

    def compare_filters(self, filters: dict[str, Any]) -> Select:
        where_clasue = []
        for field, value in filters.items():
            if not hasattr(self._model, field):
                raise AttributeError(f"Users model doesn't have {field} field")
            else:
                where_clasue.append(getattr(Users, field) == value)
        return where_clasue

    async def get(
        self,
        filters: UserGetDTO,
        lim: int = 10,
        selected_fields: list[str] = None,
    ) -> list[Users]:
        async with self.session_factory() as session:
            async with session.begin():
                base_stmt = (
                    Select(self._model)
                    if selected_fields is None
                    else self.compare_selected_fields_with_model(selected_fields)
                )
                query = base_stmt.where(
                    self.compare_filters(filters.model_dump()).limit(lim)
                )
                entities = (await session.execute(query)).scalars().all()
                return entities

    async def update(
        self, uuididf: UUID, update_data: SchemasTypes.PYDANTIC_SCHEMA_TYPE.value
    ) -> Users:
        async with self.session_factory() as session:
            try:
                stmt = (
                    Update(self._model)
                    .where(self._model.uuididf == uuididf)
                    .values(**update_data.model_dump())
                    .returning(self._model)
                )
                entity = (await session.execute(stmt)).scalar_one_or_none()
            except Exception as exc:
                await session.rollback()
                raise exc
            await session.commit()
            return entity

    async def delete(self, uuididf: UUID) -> UUID:
        async with self.session_factory() as session:
            async with session.begin():
                query = (
                    Delete(self._model)
                    .where(self._model.uuididf == uuididf)
                    .returning(self._model.uuididf)
                )
                uuididf = (await session.execute(query)).scalar_one_or_none()
                await session.commit()
                return uuididf
