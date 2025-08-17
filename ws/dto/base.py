import uuid
from pydantic import BaseModel


class BaseDTO(BaseModel):
    uuididf: uuid.UUID
