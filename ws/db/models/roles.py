from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship
from ws.db.models.base import BaseModel

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ws.db.models import Users


class Roles(BaseModel):
    __tablename__ = "roles"
    rolename: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    users: Mapped[list["Users"]] = relationship(back_populates="role")
