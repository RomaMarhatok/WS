from datetime import datetime
from sqlalchemy import MetaData, Integer, TIMESTAMP, func
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped


class BaseModel(DeclarativeBase):
    """
    Base model which represent whole base fields for each model
    """

    metadata = MetaData()

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.current_timestamp(),
    )

    @classmethod
    def group_by_fields(cls, exclude: list[str] | None = None) -> list:
        payload = []
        if not exclude:
            exclude = []
        for columns in cls.__table__.columns:
            if columns.key not in exclude:
                payload.append(payload)
        return payload
