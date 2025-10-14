import uuid
from datetime import datetime
from ws.db.models.base import BaseModel
from sqlalchemy import String, TIMESTAMP, DECIMAL, ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ws.db.models import Items, Characteristics


class CharacteristicsItems(BaseModel):
    __tablename__ = "characteristics_items"
    characteristic_uuiidf: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("characteristics.uuididf", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    item_uuiidf: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("items.uuididf", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    int_value: Mapped[float] = mapped_column(
        DECIMAL(10, 2),
        nullable=True,
        index=True,
    )
    string_value: Mapped[str] = mapped_column(
        String(150),
        nullable=True,
        index=True,
    )
    datetime_value: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=True,
        index=True,
    )
    characteristics: Mapped["Characteristics"] = relationship()
    items: Mapped[list["Items"]] = relationship(back_populates="item_characteristics")
