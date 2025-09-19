import pytest
from fastapi.exceptions import HTTPException
from ws.service.auth.registration_service import RegistrationService
from ws.service.auth.auth_service import AuthService
from ws.api.schemas.user import POSTUserRequest
from ws.api.exceptions.user import HTTP_409_CONFLICT_USERNAME_ALREADY_EXIST
from ws.db.uow.base import BaseUOW
from ws.db.repository import GenericRepository
from ws.db.models import Roles
from ws.dto.role import RoleDTO
import uuid


@pytest.fixture(scope="session")
def post_user_schema():
    return POSTUserRequest(username="Jhon", password="un@bra-cke@password")


@pytest.fixture(scope="session")
def uow(migrated_async_session_factory):
    return BaseUOW(migrated_async_session_factory)


@pytest.fixture(scope="session")
def registration_service(uow):
    return RegistrationService(uow)


@pytest.fixture(scope="session")
def authentication_service(uow):
    return AuthService(uow)


async def test_create_roles(migrated_async_session_factory):
    class Repo(GenericRepository[Roles]):
        pass

    r = Repo(migrated_async_session_factory)
    r = await r.save(RoleDTO(uuididf=uuid.uuid4(), rolename="base_user"))
    assert r.rolename == "base_user"


@pytest.mark.asyncio
async def test_register_user(
    registration_service: RegistrationService, post_user_schema: POSTUserRequest
):

    response = await registration_service.registration(post_user_schema)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_register_already_exist_user(
    registration_service: RegistrationService, post_user_schema: POSTUserRequest
):
    with pytest.raises(HTTPException) as e:
        await registration_service.registration(post_user_schema)
        assert (
            e.value.status_code == HTTP_409_CONFLICT_USERNAME_ALREADY_EXIST.status_code
        )
        assert e.value.detail == HTTP_409_CONFLICT_USERNAME_ALREADY_EXIST.detail


@pytest.mark.asyncio
async def test_auth_user(
    authentication_service: AuthService, post_user_schema: POSTUserRequest
):
    response = await authentication_service.auth(post_user_schema)
    assert response.status_code == 200
