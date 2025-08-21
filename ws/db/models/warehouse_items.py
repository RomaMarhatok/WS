import uuid
from .base import BaseModel
from sqlalchemy import UUID, Integer, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped


class WrehouseItems(BaseModel):
    __tablename__ = "warehouses_items"
    warehouses_uuididf: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("warehouses.uuididf", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    item_uuididf: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("items.uuididf", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
