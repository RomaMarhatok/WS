from .base import BaseModel
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped


class OrdertStatuses(BaseModel):
    __tablename__ = "order_statuses"
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
