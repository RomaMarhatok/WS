import uuid
from sqlalchemy import String, ForeignKey, UUID
from sqlalchemy.orm import mapped_column, Mapped
from ws.db.models.base import BaseModel


class Users(BaseModel):
    __tablename__ = "users"
    username: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(100), unique=True)
    role_uuididf: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "roles.uuididf",
            onupdate="CASCADE",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )
