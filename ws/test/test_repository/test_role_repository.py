import pytest
import pytest_asyncio
import uuid
from ws.dto import RoleDTO
from ws.db.repository import RoleRepository
from ws.db.exceptions import EntityNotFoundException, EntityAlreadyExistException


@pytest_asyncio.fixture(scope="session")
async def role_repository() -> RoleRepository:
    return RoleRepository()


@pytest_asyncio.fixture(scope="session")
async def role_dto() -> RoleDTO:
    return RoleDTO(uuididf=uuid.uuid4(), rolename="JhonVick")


@pytest_asyncio.fixture(scope="session")
async def not_exist_uuididf(role_repository: RoleRepository) -> uuid.UUID:
    uuids = [i.uuididf for i in await role_repository.get_batch()]
    not_exist_uuid = uuid.uuid4()
    while not_exist_uuid in uuids:
        not_exist_uuid = uuid.uuid4()
    return not_exist_uuid


@pytest.mark.asyncio
async def test_create_entity(role_repository: RoleRepository, role_dto: RoleDTO):
    entity = await role_repository.save(role_dto)
    assert len(await role_repository.get_batch()) == 1
    assert entity.uuididf == role_dto.uuididf
    assert entity.rolename == role_dto.rolename


@pytest.mark.asyncio
async def test_create_alredy_exist_entity(
    role_repository: RoleRepository, role_dto: RoleDTO
):
    with pytest.raises(EntityAlreadyExistException):
        await role_repository.save(role_dto)


@pytest.mark.asyncio
async def test_get_entity_by_uuididf(
    role_repository: RoleRepository, role_dto: RoleDTO
):
    entity = await role_repository.get_by_uuididf(role_dto.uuididf)
    assert entity.uuididf == role_dto.uuididf
    assert entity.rolename == role_dto.rolename


@pytest.mark.asyncio
async def test_get_not_exist_entity_by_uuididf(
    role_repository: RoleRepository, not_exist_uuididf: uuid.UUID
):
    with pytest.raises(EntityNotFoundException):
        await role_repository.get_by_uuididf(not_exist_uuididf)


@pytest.mark.asyncio
async def test_update_entity(role_repository: RoleRepository, role_dto: RoleDTO):
    role_dto.rolename += "2"
    entity = await role_repository.update(role_dto)
    assert entity.uuididf == role_dto.uuididf
    assert entity.rolename == role_dto.rolename


@pytest.mark.asyncio
async def test_delete_entity(role_repository: RoleRepository, role_dto: RoleDTO):
    await role_repository.delete(role_dto.uuididf)
    assert len(await role_repository.get_batch()) == 0


@pytest.mark.asyncio
async def test_update_not_exist_entity_by_uuididf(
    role_repository: RoleRepository, role_dto: RoleDTO, not_exist_uuididf: uuid.UUID
):
    role_dto.uuididf = not_exist_uuididf
    with pytest.raises(EntityNotFoundException):
        await role_repository.update(role_dto)
