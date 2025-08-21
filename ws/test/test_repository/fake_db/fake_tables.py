import uuid
from datetime import datetime
from sqlalchemy import MetaData, Integer, UUID, TIMESTAMP, func, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped


class FakeBaseModel(DeclarativeBase):
    metadata = MetaData()

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    uuididf: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        unique=True,
        nullable=False,
        default=uuid.uuid4,
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.current_timestamp(),
    )


class FakeAnimalTable(FakeBaseModel):
    __tablename__ = "animals"
    animal_name: Mapped[str] = mapped_column(String(100), unique=True, index=True)


class FakeOwnerTable(FakeBaseModel):
    __tablename__ = "animal_onwers"
    owner_name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    animal_uuidfidf: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("animals.uuididf", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=False,
        unique=True,
    )
