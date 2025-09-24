import uuid
from ws.dto.base import BaseDBModelDTO


class ItemDTO(BaseDBModelDTO):
    nomination: str
    description: str
    type: uuid.UUID
    type_name: str
