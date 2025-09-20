from sqlalchemy import Inspector, Connection
from ws.db.repository.reflectors.base import BaseReflector
from ws.db.types import SQLALCHEMY_MODEL_TYPE
from sqlalchemy.engine.interfaces import TableKey, ReflectedForeignKeyConstraint


class FkReflector(BaseReflector):
    def __init__(
        self,
        async_session_factory,
        tablename_filter: list[type[SQLALCHEMY_MODEL_TYPE]] = None,
    ):
        super().__init__(async_session_factory)
        self.filter = [m.__tablename__ for m in tablename_filter]

    def _get_fks_reflection(
        self, sync_conn: Connection
    ) -> dict[TableKey, list[ReflectedForeignKeyConstraint]]:
        inspector: Inspector = self._create_inspector(sync_conn)
        if self.filter is not None:
            return inspector.get_multi_foreign_keys(filter_names=self.filter)
        return inspector.get_multi_foreign_keys()

    async def get_fks_reflection(self):
        async with self.async_session_factory() as session:
            async with session.bind.connect() as conn:
                return await conn.run_sync(self._get_fks_reflection)

    async def get_field_to_which_connect(
        self,
        model_to_which_connect: type[SQLALCHEMY_MODEL_TYPE],
        tablename_which_connect: str,
    ):
        fks_reflection = (await self.get_fks_reflection()).get(
            (
                model_to_which_connect.__table__.schema,
                model_to_which_connect.__tablename__,
            )
        )
        for fk in fks_reflection:
            if fk["referred_table"] == tablename_which_connect:
                return getattr(model_to_which_connect, fk["constrained_columns"][0])

    async def get_field_that_is_connected(
        self,
        model: type[SQLALCHEMY_MODEL_TYPE],
    ):
        fks_reflection = (await self.get_fks_reflection()).get(
            (
                model.__table__.schema,
                model.__tablename__,
            )
        )
        for fk in fks_reflection:
            if fk["referred_table"] == model.__tablename__:
                return getattr(model, fk["referred_columns"][0])
