import pytest_asyncio
import uuid
import pytest
from typing import AsyncGenerator, Any
from ws.db.models import Roles
from ws.db.repository import UserRepository, RoleRepository
from ws.dto import UserDTO, RoleDTO
from ws.db.exceptions import EntityAlreadyExistException, EntityNotFoundException


@pytest_asyncio.fixture(scope="session")
async def role() -> AsyncGenerator[Any, Roles]:
    role_repo = RoleRepository()
    role_dto = RoleDTO(uuididf=uuid.uuid4(), rolename="JhonVick")
    try:
        await role_repo.delete(role_dto.uuididf)
    except EntityNotFoundException:
        pass
    role: Roles = await role_repo.save(role_dto)
    yield role
    await role_repo.delete(role.uuididf)


@pytest_asyncio.fixture(scope="session")
async def user_dto(role: Roles):
    return UserDTO(
        uuididf=uuid.uuid4(),
        username="Jhon",
        password="b027af2126c3c51bd6cec8f4490241996fc7d5f6",
        role_uuididf=role.uuididf,
    )


@pytest_asyncio.fixture
async def user_repo():
    return UserRepository()


@pytest.mark.asyncio
async def test_create_user_entity(user_repo: UserRepository, user_dto: UserDTO):
    entity = await user_repo.save(user_dto)
    assert entity.uuididf == user_dto.uuididf
    assert entity.username == user_dto.username
    assert entity.password == user_dto.password
    assert entity.role_uuididf == user_dto.role_uuididf


@pytest.mark.asyncio
async def test_create_alredy_exist_user_entity(
    user_repo: UserRepository, user_dto: UserDTO
):
    with pytest.raises(EntityAlreadyExistException):
        await user_repo.save(user_dto)


@pytest.mark.asyncio
async def test_get_user_entity_by_uuididf(user_repo: UserRepository, user_dto: UserDTO):
    entity = await user_repo.get_by_uuididf(user_dto.uuididf)
    assert entity.uuididf == user_dto.uuididf
    assert entity.username == user_dto.username
    assert entity.password == user_dto.password
    assert entity.role_uuididf == user_dto.role_uuididf


@pytest.mark.asyncio
async def test_get_not_exist_user_by_uuididf(user_repo: UserRepository):
    with pytest.raises(EntityNotFoundException):
        await user_repo.get_by_uuididf(uuid.uuid4())


@pytest.mark.asyncio
async def test_delete_user_entity(user_repo: UserRepository, user_dto: UserDTO):
    await user_repo.delete(user_dto.uuididf)
    assert len(await user_repo.get_batch()) == 0


@pytest.mark.asyncio
async def test_delete_not_exist_user_entity(
    user_repo: UserRepository, user_dto: UserDTO
):
    with pytest.raises(EntityNotFoundException):
        await user_repo.delete(user_dto.uuididf)
