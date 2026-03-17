from datetime import datetime
from ws.db.models.base import BaseModel
from sqlalchemy import String, TIMESTAMP, DECIMAL, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ws.db.models import Items, Characteristics


class CharacteristicsItems(BaseModel):
    """
    the characteristics_items table stores the values of specific item characteristics
    """

    __tablename__ = "characteristics_items"
    characteristic_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("characteristics.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    item_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("items.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    int_value: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=True, index=True)
    string_value: Mapped[str] = mapped_column(String(150), nullable=True, index=True)
    datetime_value: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=True, index=True
    )

    # backrefs
    characteristics: Mapped["Characteristics"] = relationship()
    items: Mapped[list["Items"]] = relationship(back_populates="item_characteristics")
