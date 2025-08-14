import os
import pytest
import pytest_asyncio
from typing import AsyncGenerator
from pathlib import Path
from types import SimpleNamespace
from dotenv import load_dotenv
from alembic.config import Config
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

load_dotenv(override=True)

PRJECT_ROOT = Path(__file__).parent.parent.parent.parent.resolve()


def make_alembic_config(
    cmd_opts: SimpleNamespace,
    project_root: str = PRJECT_ROOT,
) -> Config:
    # creating an absolute path for alembic.ini
    if not os.path.isabs(cmd_opts.config):
        cmd_opts.config = os.path.join(project_root, cmd_opts.config)
    # creating Config to gain access to alembic options
    config = Config(file_=cmd_opts.config, ini_section=cmd_opts.name, cmd_opts=cmd_opts)
    alembic_location = config.get_main_option("script_location")
    # also creating absolute path for 'migrations' folder
    if not os.path.isabs(alembic_location):
        config.set_main_option(
            "script_location", os.path.join(project_root, alembic_location)
        )
    if cmd_opts.db_url:
        config.set_main_option("sqlalchemy.url", cmd_opts.db_url)
    return config


@pytest.fixture(scope="session")
def neon_db_url() -> str:
    return os.environ["NEON_DB_URL"]


def alembic_config_from_url(db_url: str | None = None) -> Config:
    cmd_options = SimpleNamespace(
        config="alembic.ini",
        name="alembic",
        db_url=db_url,
        raiseerr=False,
        x=None,
    )
    return make_alembic_config(cmd_options)


@pytest.fixture(scope="session")
def alembic_config(neon_db_url) -> Config:
    return alembic_config_from_url(neon_db_url)


@pytest_asyncio.fixture(scope="session")
async def neon_async_engine(neon_db_url) -> AsyncGenerator[AsyncEngine, None]:
    engine = create_async_engine(neon_db_url)
    yield engine
    await engine.dispose()
