from pydantic import BaseModel


class GETWarehouseSchema(BaseModel):
    uuididf: str
    warehouse_name: str
