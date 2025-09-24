from ws.db.models.base import BaseModel
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ws.db.models import Items


class ItemTypes(BaseModel):
    __tablename__ = "item_types"
    name: Mapped[str] = mapped_column(String(300), unique=True, index=True)
    items: Mapped[list["Items"]] = relationship(
        "Items",
        back_populates="item_type",
    )
