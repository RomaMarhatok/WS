from ws.db.models.base import BaseModel
from sqlalchemy import Integer, ForeignKey, CheckConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ws.db.models import Warehouses, Items


class WarehouseItems(BaseModel):
    __tablename__ = "warehouses_items"
    warehouses_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("warehouses.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    item_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("items.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    amount: Mapped[int] = mapped_column(Integer, nullable=False)

    # backrefs
    warehouses: Mapped["Warehouses"] = relationship(
        back_populates="warehouse_items",
        viewonly=True,
    )
    item: Mapped["Items"] = relationship(viewonly=True)

    __table_args__ = (CheckConstraint("amount > 0", name="check_positive_amount"),)
