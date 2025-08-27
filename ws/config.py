import os
from abc import ABC, abstractmethod
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv(override=True)


class JWTTokenConfig:
    SECRET_KEY = os.environ["SECRET_KEY"]
    ALGORITHM = os.environ["ALGORITHM"]


@dataclass
class AbstractDBConfig(ABC):
    DB_NAME: str = os.environ["DB_NAME"]
    DB_USER: str = os.environ["DB_USER"]
    DB_PASSWORD: str = os.environ["DB_PASSWORD"]
    DB_HOST: str = os.environ["DB_HOST"]
    DB_PORT: str = os.environ["DB_PORT"]

    @abstractmethod
    def get_connection_string(self, driver: str):
        raise NotImplementedError


@dataclass
class PSQLDBConfig(AbstractDBConfig):
    PSQL_DEFAULT_DRIVER: str = "asyncpg"

    def get_connection_string(self, driver: str | None = None):
        psql_driver = self.PSQL_DEFAULT_DRIVER if driver is None else driver
        connection_string = (
            f"postgresql+{psql_driver}://{self.DB_USER}:{self.DB_PASSWORD}"
            + f"@{self.DB_HOST}:5432/{self.DB_NAME}"
        )
        return connection_string
