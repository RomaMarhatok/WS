from ws.db.models.base import BaseModel
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped


# TODO: Remove this model
class Characteristics(BaseModel):
    """
    characteristics table store name of each characteristic of some item
    """

    __tablename__ = "characteristics"
    name: Mapped[str] = mapped_column(String(150), unique=True, index=True)
