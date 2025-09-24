from ws.db.models.base import BaseModel
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ws.db.models import CharacteristicsItems


class Characteristics(BaseModel):
    __tablename__ = "characteristics"
    name: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    characteristics_item: Mapped[list["CharacteristicsItems"]] = relationship(
        back_populates="characteristics"
    )
