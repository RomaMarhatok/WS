import uuid
from abc import ABC
from typing import Self, Any, Callable
from ws.db.models.base import BaseModel as SQLBaseModel
from pydantic import BaseModel


class BaseDTO(BaseModel, ABC):
    @classmethod
    def from_instance(cls, instance: SQLBaseModel) -> Self:
        self = cls()
        (fields_collection, get_attr_function) = cls._get_functions(instance)
        for k in fields_collection:
            if hasattr(self, k):
                setattr(self, k, get_attr_function(instance, k))
        return self

    @classmethod
    def _get_functions(cls, instance: Any) -> tuple[list[str], Callable]:
        if issubclass(instance, SQLBaseModel):
            return (
                cls._get_instance_fields(instance),
                cls._get_instance_attr,
            )
        return (
            cls._get_dict_keys(instance),
            cls._get_dict_value,
        )

    @classmethod
    def _get_instance_fields(cls, instance: SQLBaseModel) -> list[str]:
        return instance.__table__.columns.keys()

    @classmethod
    def _get_instance_attr(cls, instance: SQLBaseModel, k: str):
        return getattr(instance, k)

    @classmethod
    def _get_dict_keys(cls, instance: dict) -> list[str]:
        return instance.keys()

    @classmethod
    def _get_dict_value(cls, instance: dict, k: str) -> list[str]:
        return instance.get(k)


class BaseDBModelDTO(BaseDTO):
    uuididf: uuid.UUID
