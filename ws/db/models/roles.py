from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped
from ws.db.models.base import BaseModel


class Roles(BaseModel):
    __tablename__ = "roles"
    rolename: Mapped[str] = mapped_column(String(100), unique=True, index=True)
