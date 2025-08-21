import uuid
from .base import BaseModel
from sqlalchemy import String, Text, UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class Items(BaseModel):
    __tablename__ = "items"
    nomination: Mapped[str] = mapped_column(String(200), unique=True, index=True)
    description: Mapped[str] = mapped_column(Text)
    type: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("item_types.uuididf", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
    )
