from typing import Protocol
from enum import Enum

from pydantic import Field, BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class DbConfProtocol(Protocol):
    @property
    def db_url(self) -> URL: ...


class AppMode(Enum):
    DEV = "DEV"
    PRODUCTION = "PROD"


class _PSQL_URL_CONFIG(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str = Field(default="localhost")
    POSTGRES_PORT: str

    @property
    def db_url(self) -> URL:
        return URL.create(
            "postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            database=self.POSTGRES_DB,
            port=self.POSTGRES_PORT,
        ).render_as_string(hide_password=False)


class _TEST_PSQL_URL_CONFIG(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    TEST_POSTGRES_DB: str
    TEST_POSTGRES_USER: str
    TEST_POSTGRES_PASSWORD: str
    TEST_POSTGRES_HOST: str = Field(default="localhost")
    TEST_POSTGRES_PORT: str

    @property
    def db_url(self) -> URL:
        return URL.create(
            "postgresql+asyncpg",
            username=self.TEST_POSTGRES_USER,
            password=self.TEST_POSTGRES_PASSWORD,
            host=self.TEST_POSTGRES_HOST,
            database=self.TEST_POSTGRES_DB,
            port=self.TEST_POSTGRES_PORT,
        ).render_as_string(hide_password=False)


class APP_CONFIG(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    APP_MODE: str


class AppConfig(BaseModel):
    APP_MODE: str
    PROD_DB_URL: str
    DEV_DB_URL: str

    @property
    def db_url(self) -> str:
        return (
            self.PROD_DB_URL
            if self.APP_MODE == AppMode.PRODUCTION.value
            else self.DEV_DB_URL
        )


app_config = AppConfig(
    APP_MODE=APP_CONFIG().APP_MODE,
    PROD_DB_URL=_PSQL_URL_CONFIG().db_url,
    DEV_DB_URL=_TEST_PSQL_URL_CONFIG().db_url,
)
