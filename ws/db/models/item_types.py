from .base import BaseModel
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped


class ItemTypes(BaseModel):
    __tablename__ = "item_types"
    name: Mapped[str] = mapped_column(String(300), unique=True, index=True)
