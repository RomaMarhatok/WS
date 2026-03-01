import uuid
from abc import ABC
from typing import Self, Any, Callable
from ws.db.models.base import BaseModel as SQLBaseModel
from pydantic import BaseModel, ValidationError


class BaseDTO(BaseModel, ABC):
    @classmethod
    def from_instance(cls, instance: SQLBaseModel) -> Self:
        """parse fields which only need for DTO"""
        fields_from_instance = {}
        (fields_collection, get_attr_function) = cls._get_functions(instance)
        for k in fields_collection:
            if k in cls.model_fields:
                fields_from_instance.update({k: get_attr_function(instance, k)})
        try:
            dto_inst = cls(**fields_from_instance)
        except ValidationError as e:
            missed_required_fields = [err["loc"][0] for err in e.errors()]
            raise AttributeError(
                "You have not sent these required fields to dto "
                + f"{",".join(missed_required_fields)}"
            )
        return dto_inst

    @classmethod
    def _get_functions(cls, instance: Any) -> tuple[list[str], Callable]:
        if issubclass(type(instance), SQLBaseModel):
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

    def __eq__(self, value: SQLBaseModel):
        if not isinstance(value, SQLBaseModel):
            raise TypeError(
                f"For compare model with dto it must inherit from {SQLBaseModel.__name__}"
            )
        fields = list(self.__class__.model_fields.keys())
        for f in fields:
            if not hasattr(value, f):
                raise AttributeError(f"{value.__name__} doesn' have attribute {f}")
            if not (getattr(value, f) == getattr(self, f)):
                return False
        return True
