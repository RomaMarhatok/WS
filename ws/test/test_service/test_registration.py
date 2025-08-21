import pytest
from fastapi.exceptions import HTTPException
from ws.service.registration_service import RegistrationService
from ws.api.schemas.user import POSTUserSchema
from ws.api.exceptions import HTTP_409_CONFLICT_USERNAME_ALREADY_EXIST


@pytest.fixture(scope="session")
def post_user_schema():
    return POSTUserSchema(username="Jhon", password="un@bra-cke@password")


@pytest.fixture(scope="session")
def registration_service():
    return RegistrationService()


@pytest.mark.asyncio
async def test_register_user(
    registration_service: RegistrationService, post_user_schema: POSTUserSchema
):
    response = await registration_service.registration(post_user_schema)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_register_already_exist_user(
    registration_service: RegistrationService, post_user_schema: POSTUserSchema
):
    with pytest.raises(HTTPException) as e:
        await registration_service.registration(post_user_schema)
        assert (
            e.value.status_code == HTTP_409_CONFLICT_USERNAME_ALREADY_EXIST.status_code
        )
        assert e.value.detail == HTTP_409_CONFLICT_USERNAME_ALREADY_EXIST.detail
