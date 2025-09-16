import os
from abc import ABC, abstractmethod
from dotenv import load_dotenv
from dataclasses import dataclass
from datetime import timedelta

load_dotenv(override=True)


class JWTTokenConfig:
    SECRET_KEY = os.environ["SECRET_KEY"]
    ALGORITHM = os.environ["ALGORITHM"]
    ACCESS_TOKEN_TIMEDELTA = timedelta(minutes=30)
    REFRESH_TOKEN_TIMEDELTA = timedelta(days=1)


# must create some type of singleton which can share state between env.py and conftest.py
class AbstractDBConfig(ABC):

    def __init__(self, DB_NAME: str, DB_USER: str, DB_PASSWORD: str, DB_HOST: str):
        self.DB_NAME = DB_NAME
        self.DB_USER = DB_USER
        self.DB_PASSWORD = DB_PASSWORD
        self.DB_HOST = DB_HOST

    @abstractmethod
    def get_connection_string(self, driver: str):
        raise NotImplementedError


@dataclass
class PSQLDBConfig(AbstractDBConfig):

    def __init__(
        self,
        DB_NAME: str,
        DB_USER: str,
        DB_PASSWORD: str,
        DB_HOST: str,
        PSQL_DRIVER: str = "asyncpg",
    ):
        super().__init__(
            DB_NAME,
            DB_USER,
            DB_PASSWORD,
            DB_HOST,
        )
        self.PSQL_DRIVER = PSQL_DRIVER

    def get_connection_string(self):
        connection_string = (
            f"postgresql+{self.PSQL_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}"
            + f"@{self.DB_HOST}:5432/{self.DB_NAME}"
        )
        return connection_string


class DBConnectionStringController:
    def get_config(self) -> AbstractDBConfig:
        if bool(os.environ["TEST_ENV"]):
            return PSQLDBConfig(
                DB_NAME=os.environ["TEST_DB_NAME"],
                DB_HOST=os.environ["TEST_DB_HOST"],
                DB_USER=os.environ["DB_USER"],
                DB_PASSWORD=os.environ["DB_PASSWORD"],
            )

        return PSQLDBConfig(
            DB_NAME=os.environ["DB_NAME"],
            DB_USER=os.environ["DB_USER"],
            DB_PASSWORD=os.environ["DB_PASSWORD"],
            DB_HOST=os.environ["DB_HOST"],
        )
