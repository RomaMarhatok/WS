import uuid
from .base import BaseModel
from sqlalchemy import UUID, ForeignKey, String
from sqlalchemy.orm import mapped_column, Mapped


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
        nullable=False,
    )
