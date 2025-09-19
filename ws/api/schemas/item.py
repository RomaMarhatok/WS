import uuid
from pydantic import BaseModel


class GETItemResponse(BaseModel):
    uuididf: uuid.UUID
    nomination: str
    description: str
    type: str


class GETItemsListResponse:
    items: list[GETItemResponse]
