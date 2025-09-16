from fastapi.exceptions import HTTPException
from ws.db.uow.base import BaseUOW
from utils.decorators import handle_http_exceptions


class BaseService:
    def __init__(
        self, db_to_http_exception_map: dict[Exception, HTTPException], uow: BaseUOW
    ):
        self.db_to_http_exception_map = db_to_http_exception_map
        self.uow = uow

    def __getattribute__(self, name: str):
        return handle_http_exceptions(self.db_to_http_exception_map)(
            super().__getattribute__(name)
        )
