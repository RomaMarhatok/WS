import pytest
from ws.db.repository._generic_repository import GenericRepository
from ws.db.models import Roles, Users


@pytest.fixture
def repository_role_fixture(db_session_factory):
    class RoleRepository(GenericRepository[Roles]):
        pass

    return RoleRepository(db_session_factory)


@pytest.fixture
def repository_user_fixture(db_session_factory):
    class UserRepository(GenericRepository[Users]):
        pass

    return UserRepository(db_session_factory)
