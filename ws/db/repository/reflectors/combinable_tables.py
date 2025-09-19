from collections import UserList
from sqlalchemy.engine.interfaces import TableKey, ReflectedForeignKeyConstraint
from ws.db.types import SQLALCHEMY_MODEL_TYPE
from ws.db.repository.exceptions import (
    NotCombinedTablesException,
    InvalidTableOrderException,
)


class CombineInfo:
    def __init__(
        self,
        tablename: str,
        constrained_column: str,
        reffered_table: str,
        reffered_column: str,
    ):
        self.tablename = tablename
        self.constrained_column = constrained_column
        self.reffered_table = reffered_table
        self.reffered_column = reffered_column


class IsCombinable:
    def __init__(
        self,
        is_combinable: bool,
        table_to_which_they_are_attached: CombineInfo,
    ):
        self.is_combinable = is_combinable
        self.table_to_which_they_are_attached = table_to_which_they_are_attached

    def __bool__(self):
        return self.is_combinable


class CombinableList(UserList):
    def __init__(
        self,
        fks_reflection: dict[TableKey, list[ReflectedForeignKeyConstraint]],
        models: list[SQLALCHEMY_MODEL_TYPE],
    ):
        self._fks_reflection = fks_reflection
        if self.check_tables_is_joinable(models) and self.check_tables_order(models):
            super().__init__(models)

    def check_tables_is_joinable(self, models: list[SQLALCHEMY_MODEL_TYPE]) -> bool:
        for i in range(len(models)):
            if i + 1 >= len(models):
                break
            current_m, next_m = models[i], models[i + 1]
            if not self._check_tables_is_joinable(
                current_m, next_m, self._fks_reflection
            ):
                raise NotCombinedTablesException(
                    f"Table {current_m.__tablename__} and {next_m.__tablename__}"
                    + "are not combinable"
                )
            current_m, next_m = next_m, models[i + 1]
        return True

    def check_tables_order(self, models: list[SQLALCHEMY_MODEL_TYPE]):
        if len(models) <= 1:
            raise ValueError(f"Use {self.__class__.__name__} at least for two models")
        model_iter = iter(models)
        current_m, next_m = next(model_iter), next(model_iter)
        while True:
            table_fk_reflection = self._fks_reflection.get(
                (current_m.__table__.schema, current_m.__tablename__)
            )
            for fk in table_fk_reflection:
                if fk["referred_table"] == next_m.__tablename__:
                    return True
            try:
                current_m, next_m = next_m, next(model_iter)
            except StopIteration:
                raise InvalidTableOrderException(
                    "Invalid order of tables passed as parameter"
                    + f"The table {current_m.__tablename__} don't "
                    + f"have any relationships with {next_m.__tablename__}"
                )

    def devide_tables_by_pare(
        self,
    ) -> list[tuple[type[SQLALCHEMY_MODEL_TYPE], type[SQLALCHEMY_MODEL_TYPE]]]:
        try:
            models_iter = iter(self.data)
            current_m, next_m = next(models_iter), next(models_iter)
            pare_list = [(current_m, next_m)]
            while True:
                current_m, next_m = next_m, next(models_iter)
                pare_list.append((current_m, next_m))
        except StopIteration:
            return pare_list

    def _check_tables_is_joinable(
        self,
        left_model: type[SQLALCHEMY_MODEL_TYPE],
        right_model: type[SQLALCHEMY_MODEL_TYPE],
        fks_reflection: dict[TableKey, list[ReflectedForeignKeyConstraint]],
    ) -> bool:
        left_fks = fks_reflection.get(
            (left_model.__table__.schema, left_model.__tablename__)
        )
        right_fks = fks_reflection.get(
            (right_model.__table__.schema, right_model.__tablename__)
        )
        if left_fks is None or right_fks is None:
            return False
        left_iter = iter(min([left_fks, right_fks], key=len))
        right_iter = iter(max([left_fks, right_fks], key=len))
        while True:
            try:
                left_fk = next(left_iter)
                if left_fk["referred_table"] == right_model.__tablename__:
                    return True
            except StopIteration:
                pass
            try:
                right_fk = next(right_iter)
                if right_fk["referred_table"] == left_model.__tablename__:
                    return True
            except StopIteration:
                return False
