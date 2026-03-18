import pytest
from faker import Faker
from ws.api.v1.schemas.role import CreateRoleDTO


@pytest.fixture
async def create_role_dto(fake_data_generator: Faker) -> CreateRoleDTO:
    return CreateRoleDTO(rolename=fake_data_generator.name())
