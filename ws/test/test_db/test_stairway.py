import pytest
from alembic.config import Config
from alembic.command import downgrade, upgrade
from alembic.script import Script, ScriptDirectory
from ws.test.test_db.conftest import alembic_config_from_url


def get_revisions() -> list[Script]:
    config = alembic_config_from_url()
    revisions_dir = ScriptDirectory.from_config(config)
    revisions = list(revisions_dir.walk_revisions("base", "heads"))
    revisions.reverse()
    return revisions


@pytest.mark.parametrize("revision", get_revisions())
def test_migrations_stairway(alembic_config: Config, revision: Script):
    upgrade(alembic_config, revision.revision)

    # We need -1 for downgrading first migration (its down_revision is None)
    downgrade(alembic_config, revision.down_revision or "-1")
    upgrade(alembic_config, revision.revision)
