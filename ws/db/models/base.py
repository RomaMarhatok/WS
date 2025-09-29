import uuid
from datetime import datetime
from typing import Any, Self
from sqlalchemy import MetaData, Integer, UUID, TIMESTAMP, func
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, Mapper
from sqlalchemy.inspection import inspect
from sqlalchemy.orm.relationships import RelationshipProperty


class BaseModel(DeclarativeBase):
    metadata = MetaData()

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    uuididf: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        unique=True,
        nullable=False,
        default=uuid.uuid4,
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.current_timestamp(),
    )

    @classmethod
    def _get_self_inspector(cls) -> Mapper:
        return inspect(cls)

    @classmethod
    def get_model_relationships(cls) -> list[RelationshipProperty[Any]]:
        return cls._get_self_inspector().relationships.values()

    @classmethod
    def _get_relationships_graph(
        cls,
        initial_dict: dict[type[Self], list[RelationshipProperty[Any]]],
    ):
        if cls not in initial_dict:
            initial_dict.update({cls: cls.get_model_relationships()})
        for relationship in initial_dict[cls]:
            next_class = relationship.mapper.class_
            if next_class in initial_dict:
                continue
            if isinstance(next_class, BaseModel):
                initial_dict.update({next_class: next_class.get_model_relationships()})
            initial_dict.update(next_class._get_relationships_graph(initial_dict))
        return initial_dict

    @classmethod
    def get_relationships_graph(cls):
        relationships_graph: dict[Self, list] = {cls: cls.get_model_relationships()}
        relationships_graph.update(cls._get_relationships_graph(relationships_graph))
        return relationships_graph
