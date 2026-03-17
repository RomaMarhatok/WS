from ws.db.models.base import BaseModel
from sqlalchemy import ForeignKey, Integer, Text, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ws.db.models import OrderStatuses, Items, Warehouses, Users


class Orders(BaseModel):
    __tablename__ = "orders"
    order_status_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("order_statuses.id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    item_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("items.id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    warehouse_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("warehouses.id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    customer_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    order_status: Mapped["OrderStatuses"] = relationship(
        "OrderStatuses", back_populates="orders"
    )
    amount: Mapped[int] = mapped_column(Integer)

    # backrefs
    item: Mapped["Items"] = relationship()
    warehouse: Mapped["Warehouses"] = relationship()
    customer: Mapped["Users"] = relationship()
    description: Mapped[str] = mapped_column(Text, nullable=True)

    __table_args__ = (CheckConstraint("amount > 0", name="check_positive_amount"),)
