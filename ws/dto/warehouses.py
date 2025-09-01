import uuid
from ws.dto.base import BaseDBModelDTO


class WarehousesDTO(BaseDBModelDTO):
    warehouse_name: str
    warehouse_worker_uuididf: uuid.UUID
