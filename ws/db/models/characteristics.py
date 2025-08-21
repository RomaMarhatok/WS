from .base import BaseModel
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped


class Characteristics(BaseModel):
    __tablename__ = "characteristics"
    name: Mapped[str] = mapped_column(String(150), unique=True, index=True)
