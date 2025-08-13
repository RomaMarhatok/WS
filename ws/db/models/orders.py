import uuid
from .base import BaseModel
from sqlalchemy import ForeignKey, UUID, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column


class Orders(BaseModel):
    __tablename__ = "orders"
    status_uuididf: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey("order_statuses.uuididf", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    item_uuididf: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey("items.uuididf", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    warehouse_uuididf: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey("warehouses.uuididf", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    customer_uuididf: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey("users.uuididf", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    amount: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(Text, nullable=True)
