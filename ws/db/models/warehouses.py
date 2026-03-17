from typing import TYPE_CHECKING
from sqlalchemy import Integer, ForeignKey, String
from sqlalchemy.orm import mapped_column, Mapped, relationship
from ws.db.models.base import BaseModel

if TYPE_CHECKING:
    from ws.db.models import WarehouseItems


class Warehouses(BaseModel):
    __tablename__ = "warehouses"
    warehouse_name: Mapped[str] = mapped_column(String(200), unique=True, index=True)
    warehouse_worker_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
    )

    # backrefs
    warehouse_items: Mapped[list["WarehouseItems"]] = relationship(
        back_populates="warehouses", viewonly=True
    )
