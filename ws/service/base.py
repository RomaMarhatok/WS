from fastapi.exceptions import HTTPException
from types import MethodType
from ws.db.uow.base import BaseUOW
from ws.utils.decorators import handle_http_exceptions


class BaseService:
    def __init__(
        self, db_to_http_exception_map: dict[Exception, HTTPException], uow: BaseUOW
    ):
        self._db_to_http_exception_map = db_to_http_exception_map
        self.uow = uow

    def __getattribute__(self, name: str):
        if name == "_db_to_http_exception_map":
            return super().__getattribute__(name)
        atr = super().__getattribute__(name)
        if isinstance(atr, MethodType):
            return handle_http_exceptions(self._db_to_http_exception_map)(atr)
        return atr
