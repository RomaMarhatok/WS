from typing import TypeVar
from ws.dto.base import BaseDBModelDTO
from ws.db.models import BaseModel

PYDANTIC_SCHEMA_TYPE = TypeVar("PYDANTIC_SCHEMA_TYPE", bound=BaseDBModelDTO)
SQLALCHEMY_MODEL_TYPE = TypeVar("SQLALCHEMY_MODEL_TYPE", bound=BaseModel)
