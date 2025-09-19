from fastapi import APIRouter, Depends
from service.warehouse_service import WarehousesService
from api.dependencies import get_warehouse_serivce
from schemas.warehouse import GETWarehouseRequest
from ws.dto import WarehousesDTO

warehouse_router = APIRouter(prefix="warehouse/")


@warehouse_router.get("warehouse/", response_model=WarehousesDTO)
async def get_warehouse(
    request: GETWarehouseRequest,
    warehouse_service: WarehousesService = Depends(get_warehouse_serivce),
):
    warehouse_dto = await warehouse_service.get_one_warehouses(request)
    return warehouse_dto


@warehouse_router.get("warehouse/items/")
async def get_warehouse_items(
    request: GETWarehouseRequest,
    warehouse_service: WarehousesService = Depends(get_warehouse_serivce),
):
    warehouse_service.get_one_warehouses
