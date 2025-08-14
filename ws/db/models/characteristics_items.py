import uuid
from datetime import datetime
from .base import BaseModel
from sqlalchemy import String, TIMESTAMP, DECIMAL, ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column


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
