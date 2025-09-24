from typing import Optional
from pydantic import BaseModel


class GETWarehouseRequest(BaseModel):
    uuididf: str
    warehouse_name: Optional[str] = None
