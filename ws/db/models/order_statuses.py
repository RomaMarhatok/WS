from ws.db.models.base import BaseModel
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ws.db.models import Orders


class OrderStatuses(BaseModel):
    __tablename__ = "order_statuses"
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    orders: Mapped[list["Orders"]] = relationship(
        "Orders", back_populates="order_status"
    )
