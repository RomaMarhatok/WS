from fastapi import APIRouter, Depends
from service.warehouse_service import WarehousesService
from api.dependencies import get_warehouse_serivce
from schemas.warehouse import GETWarehouseSchema

warehouse_router = APIRouter(prefix="warehouse")


@warehouse_router.get("/warehouse/")
async def get_warehouse(
    request: GETWarehouseSchema,
    warehouse_service: WarehousesService = Depends(get_warehouse_serivce),
):
    warehouse_dto = await warehouse_service.get_one_warehouses(request)
    return warehouse_dto.model_dump()
