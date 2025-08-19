import os
from pathlib import Path
from types import SimpleNamespace
from alembic.config import Config
from dotenv import load_dotenv

load_dotenv(override=True)

PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()


def make_alembic_config(
    cmd_opts: SimpleNamespace,
    project_root: str = PROJECT_ROOT,
) -> Config:
    # creating an absolute path for alembic.ini
    if not os.path.isabs(cmd_opts.config):
        cmd_opts.config = os.path.join(project_root, cmd_opts.config)
    # creating Config to gain access to alembic options
    config = Config(file_=cmd_opts.config, ini_section=cmd_opts.name, cmd_opts=cmd_opts)
    alembic_location = config.get_main_option("script_location")
    print("SCRIPT LOCATION", alembic_location)
    print("ROOT", alembic_location)

    # getting flags after -x tag in alembic command line interface
    # also creating absolute path for 'migrations' folder
    if not os.path.isabs(alembic_location):
        print("IF")
        config.set_main_option(
            "script_location", os.path.join(project_root, alembic_location)
        )
    if cmd_opts.testing:
        alembic_location = os.path.join(
            project_root,
            "ws\\test\\test_repository\\fake_db\\fake_alembic\\migrations",
        )
        print("ROOT@", project_root)
        print("alembic location", alembic_location)
        config.set_main_option("script_location", alembic_location)
    print("SCRIPT LOCATION", config.get_main_option("script_location"))

    if cmd_opts.db_url:
        config.set_main_option("sqlalchemy.url", cmd_opts.db_url)
    return config


def alembic_config_from_url(
    alembic_ini_file_name: str = "alembic.ini",
    section_name_in_alembic_ini_file: str = "alembic",
    db_url: str | None = None,
    testing: bool = False,
) -> Config:
    cmd_options = SimpleNamespace(
        config=alembic_ini_file_name,
        name=section_name_in_alembic_ini_file,
        db_url=db_url,
        testing=testing,
        raiseerr=False,
        x=None,
    )
    return make_alembic_config(cmd_options)
