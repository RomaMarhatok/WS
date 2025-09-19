from sqlalchemy import Inspector, Connection
from ws.db.repository.reflectors.base import BaseReflector
from ws.db.types import SQLALCHEMY_MODEL_TYPE
from sqlalchemy.engine.interfaces import TableKey, ReflectedForeignKeyConstraint


class FkReflector(BaseReflector):
    def __init__(self, async_session_factory, tablename_filter: list[str] = None):
        super().__init__(async_session_factory)
        self.tablename_filter = tablename_filter

    def _get_fks_reflection(
        self, sync_conn: Connection
    ) -> dict[TableKey, list[ReflectedForeignKeyConstraint]]:
        inspector: Inspector = self._create_inspector(sync_conn)
        if self.tablename_filter is not None:
            return inspector.get_multi_foreign_keys(filter_names=self.tablename_filter)
        return inspector.get_multi_foreign_keys()

    async def get_fks_reflection(self):
        async with self.async_session_factory().bind.engine.connect() as conn:
            return await conn.run_sync(self._get_fks_reflection)

    async def check_tables_is_joinable(
        self, left_tablename: str, right_tablename: str
    ) -> bool:
        fks_reflection = await self.get_fks_reflection()
        for (_, tablename), fks in fks_reflection:
            for fk in fks:
                if "referred_table" in fk and (
                    fk["referred_table"] == right_tablename
                    or fk["referred_table"] == left_tablename
                ):
                    return True
        return False

    async def get_field_to_which_connect(self, model: type[SQLALCHEMY_MODEL_TYPE]):
        fks_reflection = await self.get_fks_reflection()
        for (_, tablename), fks in fks_reflection:
            if fks["referred_table"] == model.__tablename__:
                return getattr(model, fks["constrained_columns"][0])

    async def get_field_that_is_connected(self, model: type[SQLALCHEMY_MODEL_TYPE]):
        fks_reflection = await self.get_fks_reflection()
        for (_, tablename), fks in fks_reflection:
            if fks["referred_table"] == model.__tablename__:
                return getattr(model, fks["referred_columns"][0])
