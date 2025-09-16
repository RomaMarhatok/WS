from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from ws.api.schemas import ListPaginationSchema, GETWarehouseSchema
from ws.api.exceptions.base import HTTP_404_RECORD_NOT_FOUND
from db.exceptions import EntityNotFoundException
from service.base import BaseService
from ws.db.uow.base import BaseUOW


db_to_http_exception_map = {EntityNotFoundException: HTTP_404_RECORD_NOT_FOUND}


class WarehousesService(BaseService):

    def __init__(
        self, uow: BaseUOW, db_to_http_exception_map: dict[Exception, HTTPException]
    ):
        super().__init__(db_to_http_exception_map=db_to_http_exception_map, uow=uow)

    async def get_all_warehouses(self, pagination: ListPaginationSchema):
        warehouses_list = await self.uow.warehouses.get_all(**pagination.model_dump())
        return JSONResponse(content={"warehouses": warehouses_list})

    async def get_one_warehouses(self, warehouse: GETWarehouseSchema):
        warehouse_dto = await self.uow.warehouses.get_warehouse(
            **warehouse.model_dump()
        )
