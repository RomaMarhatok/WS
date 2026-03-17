from ws.db.models.base import BaseModel
from sqlalchemy import String, Text, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ws.db.models import (
        ItemTypes,
        CharacteristicsItems,
    )


class Items(BaseModel):
    __tablename__ = "items"
    nomination: Mapped[str] = mapped_column(String(200), unique=True, index=True)
    description: Mapped[str] = mapped_column(Text)
    type_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("item_types.id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
    )

    # backrefs
    item_type: Mapped["ItemTypes"] = relationship()
    item_characteristics: Mapped[list["CharacteristicsItems"]] = relationship(
        "CharacteristicsItems", back_populates="items"
    )
