from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import mapped_column, Mapped, relationship
from ws.db.models.base import BaseModel

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ws.db.models import Roles


class Users(BaseModel):
    __tablename__ = "users"
    username: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(100), unique=True)
    role_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("roles.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )

    # backrefs
    role: Mapped["Roles"] = relationship(back_populates="users")
