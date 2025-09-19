from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from ws.api.schemas import ListPaginationSchema, GETWarehouseRequest
from ws.api.exceptions.base import HTTP_404_RECORD_NOT_FOUND
from ws.db.repository.exceptions import EntityNotFoundException
from service.base import BaseService
from ws.db.uow.base import BaseUOW


class WarehousesService(BaseService):

    def __init__(
        self,
        uow: BaseUOW,
        db_to_http_exception_map: dict[Exception, HTTPException] = {
            EntityNotFoundException: HTTP_404_RECORD_NOT_FOUND
        },
    ):
        super().__init__(db_to_http_exception_map=db_to_http_exception_map, uow=uow)

    async def get_all_warehouses(self, pagination: ListPaginationSchema):
        warehouses_list = await self.uow.warehouses.get_all(**pagination.model_dump())
        return JSONResponse(content={"warehouses": warehouses_list})

    async def get_one_warehouses(self, warehouse: GETWarehouseRequest):
        warehouse_dto = await self.uow.warehouses.get_warehouse(
            **warehouse.model_dump(exclude_none=True)
        )
        return warehouse_dto

    async def get_warehouse_items(self, warehouse: GETWarehouseRequest):
        await self.uow.warehouse_items.get_warehouse_items(
            **warehouse.model_dump(exclude_none=True)
        )
