from typing import TypeVar
from pydantic import BaseModel as PyadanticBaseModel
from ws.db.models import BaseModel

PYDANTIC_SCHEMA_TYPE = TypeVar("PYDANTIC_SCHEMA_TYPE", bound=PyadanticBaseModel)
SQLALCHEMY_MODEL_TYPE = TypeVar("SQLALCHEMY_MODEL_TYPE", bound=BaseModel)
