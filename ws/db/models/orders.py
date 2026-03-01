import uuid
from ws.db.models.base import BaseModel
from sqlalchemy import ForeignKey, UUID, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ws.db.models import OrderStatuses, Items, Warehouses, Users


class Orders(BaseModel):
    __tablename__ = "orders"
    status_uuididf: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("order_statuses.uuididf", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    item_uuididf: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("items.uuididf", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    warehouse_uuididf: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("warehouses.uuididf", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    customer_uuididf: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.uuididf", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    order_status: Mapped["OrderStatuses"] = relationship(
        "OrderStatuses", back_populates="orders"
    )

    # backrefs
    item: Mapped["Items"] = relationship()
    warehouse: Mapped["Warehouses"] = relationship()
    customer: Mapped["Users"] = relationship()
    amount: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(Text, nullable=True)
