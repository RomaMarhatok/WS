import uuid
from ws.api.v1.schemas.base import BaseDBModelDTO


class ItemDTO(BaseDBModelDTO):
    nomination: str
    description: str
    type: uuid.UUID
    type_name: str
