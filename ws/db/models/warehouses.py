import uuid
from ws.db.models.base import BaseModel
from sqlalchemy import UUID, ForeignKey, String
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ws.db.models import Items, WarehouseItems


class Warehouses(BaseModel):
    __tablename__ = "warehouses"
    warehouse_name: Mapped[str] = mapped_column(String(200), unique=True, index=True)
    warehouse_worker_uuididf: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "users.uuididf",
            onupdate="CASCADE",
            ondelete="SET NULL",
        ),
        nullable=True,
    )
    warehouse_items: Mapped[list["WarehouseItems"]] = relationship(
        back_populates="warehouses", viewonly=True
    )
    items: Mapped[list["Items"]] = relationship(
        secondary="warehouses_items", back_populates="warehouses"
    )
