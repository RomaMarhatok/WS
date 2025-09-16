from abc import ABC
from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from ws.db.repository import GenericRepository
from ws.db.types import SQLALCHEMY_MODEL_TYPE


class BaseCommandsManager(ABC):
    """BaseCommandManager class handles commands that implement
    the logiсal part of query managment which refer to many db tables

    Attributes:
        session_factory (async_sessionmaker[AsyncSession]): Factory for creation
        SQLALchemy async database session
    Methods:
        get_repository(model: Type[SQLALCHEMY_MODEL_TYPE])
        -> GenericRepository[SQLALCHEMY_MODEL_TYPE]:
            Returns a repostiroy instance tailored for to specified SQLAlchemy model
    """

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self.session_factory = session_factory

    def get_repository(
        self, model: Type[SQLALCHEMY_MODEL_TYPE]
    ) -> GenericRepository[SQLALCHEMY_MODEL_TYPE]:
        class Repository(GenericRepository[model]):
            pass

        return Repository(self.session_factory)
