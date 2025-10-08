import pytest
from ws.db.repository.base_repository import GenericRepository
from ws.db.models import Roles


@pytest.fixture
def repository_role_fixture(db_session_factory):
    class RoleRepository(GenericRepository[Roles]):
        pass

    return RoleRepository(db_session_factory)
