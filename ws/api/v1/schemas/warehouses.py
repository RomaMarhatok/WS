import uuid
from ws.api.v1.schemas.base import BaseDBModelDTO


class WarehousesDTO(BaseDBModelDTO):
    warehouse_name: str
    warehouse_worker_uuididf: uuid.UUID
