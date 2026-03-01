from enum import Enum
from typing import TypeVar
from ws.db.models import BaseModel
from pydantic import BaseModel as PydanticBaseModel


class SchemasTypes(Enum):
    PYDANTIC_SCHEMA_TYPE = TypeVar("PYDANTIC_SCHEMA_TYPE", bound=PydanticBaseModel)
    SQLALCHEMY_MODEL_TYPE = TypeVar("SQLALCHEMY_MODEL_TYPE", bound=BaseModel)
