import uuid
from ws.db.models.base import BaseModel
from sqlalchemy import UUID, Integer, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ws.db.models import Warehouses


class WarehouseItems(BaseModel):
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
    warehouses: Mapped["Warehouses"] = relationship(
        "Warehouses", back_populates="warehouse_items"
    )
