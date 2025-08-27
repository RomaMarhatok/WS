import pytest
import uuid
import pytest_asyncio
from ws.db.repository.base_repository import GenericRepository
from ws.db.exceptions import (
    EntityAlreadyExistException,
    EntityNotFoundException,
    ForeignKeyNotExist,
)
from ws.db.models import Roles, Users
from ws.dto import UserDTO, RoleDTO


@pytest.fixture(scope="session")
def role_repository(async_session_factory):
    class RoleRepository(GenericRepository[Roles]):
        pass

    return RoleRepository(async_session_factory())


@pytest.fixture(scope="session")
def user_repository(async_session_factory):
    class UserRepository(GenericRepository[Users]):
        pass

    return UserRepository(async_session_factory())


@pytest.fixture(scope="session")
def role_dto() -> RoleDTO:
    return RoleDTO(uuididf=uuid.uuid4(), rolename="boby")


@pytest_asyncio.fixture(scope="session")
async def role_from_db(
    role_repository: GenericRepository[Roles],
    role_dto: RoleDTO,
) -> Roles:
    return await role_repository.save(role_dto)


@pytest.fixture(scope="session")
def user_dto(role_from_db: Roles) -> UserDTO:
    return UserDTO(
        uuididf=uuid.uuid4(),
        username="Tom",
        role_uuididf=role_from_db.uuididf,
    )


@pytest.mark.asyncio
async def test_create_role_entity(
    role_repository: GenericRepository[Roles],
    role_dto: RoleDTO,
):
    entity = await role_repository.save(role_dto)
    assert len(await role_repository.get_batch()) == 1
    assert entity.uuididf == role_dto.uuididf
    assert entity.rolename == role_dto.rolename


@pytest.mark.asyncio
async def test_create_already_exist_role_entity(
    role_repository: GenericRepository[Roles],
    role_dto: RoleDTO,
):
    with pytest.raises(EntityAlreadyExistException):
        await role_repository.save(role_dto)


@pytest.mark.asyncio
async def test_get_role_by_uuididf(
    role_repository: GenericRepository[Roles],
    role_dto: RoleDTO,
):
    entity = await role_repository.get(uuididf=role_dto.uuididf)
    assert entity.uuididf == role_dto.uuididf
    assert entity.rolename == role_dto.rolename


@pytest.mark.asyncio
async def test_get_role_by_name(
    role_repository: GenericRepository[Roles],
    role_dto: RoleDTO,
):
    entity = await role_repository.get(rolename=role_dto.rolename)
    assert entity.uuididf == role_dto.uuididf
    assert entity.rolename == role_dto.rolename


@pytest.mark.asyncio
async def test_get_role_by_name_with_field(
    role_repository: GenericRepository[Roles],
    role_dto: RoleDTO,
):

    entity = await role_repository.get(rolename=role_dto.rolename)
    assert entity.uuididf == role_dto.uuididf
    assert entity.rolename == role_dto.rolename


@pytest.mark.asyncio
async def test_get_not_exist_role_by_uuididf(
    role_repository: GenericRepository[Roles],
):
    with pytest.raises(EntityNotFoundException):
        await role_repository.get(uuididf=uuid.uuid4())


@pytest.mark.asyncio
async def test_get_not_exist_role_by_name(
    role_repository: GenericRepository[Roles],
):
    with pytest.raises(EntityNotFoundException):
        await role_repository.get(rolename="Cat")


@pytest.mark.asyncio
async def test_multiply_kwarg_in_get_method(
    role_repository: GenericRepository[Roles],
):
    with pytest.raises(ValueError):
        await role_repository.get(rolename="Cat", uuididf=uuid.uuid4())


@pytest.mark.asyncio
async def test_get_role_by_not_exist_field(
    role_repository: GenericRepository[Roles],
):
    with pytest.raises(AttributeError):
        await role_repository.get(not_exist_field="Cat")


@pytest.mark.asyncio
async def test_find_role_use_find_method(
    role_repository: GenericRepository[Roles],
    role_dto: RoleDTO,
):
    entities = await role_repository.find(
        rolename=role_dto.rolename, uuididf=role_dto.uuididf
    )
    assert len(entities) != 0
    assert entities[0].uuididf == role_dto.uuididf
    assert entities[0].rolename == role_dto.rolename


@pytest.mark.asyncio
async def test_find_role_with_not_exist_fields_method(
    role_repository: GenericRepository[Roles],
    role_dto: RoleDTO,
):
    with pytest.raises(AttributeError):
        await role_repository.find(
            not_exist_field=role_dto.rolename, uuididf=role_dto.uuididf
        )


@pytest.mark.asyncio
async def test_find_role_without_argument(
    role_repository: GenericRepository[Roles],
):
    with pytest.raises(AttributeError):
        await role_repository.find()


@pytest.mark.asyncio
async def test_update_role(
    role_repository: GenericRepository[Roles],
    role_dto: RoleDTO,
):
    role_dto.rolename = "foxy"
    entity = await role_repository.update(role_dto)
    assert entity.uuididf == role_dto.uuididf
    assert entity.rolename == role_dto.rolename


@pytest.mark.asyncio
async def test_update_not_exist_entity(
    role_repository: GenericRepository[Roles],
):
    role_dto = RoleDTO(uuididf=uuid.uuid4(), rolename="boby")
    with pytest.raises(EntityNotFoundException):
        await role_repository.update(role_dto)


@pytest.mark.asyncio
async def test_delete_role_entity(
    role_repository: GenericRepository[Roles],
    role_dto: RoleDTO,
):

    await role_repository.delete(role_dto.uuididf)
    assert len(await role_repository.get_batch()) == 0


@pytest.mark.asyncio
async def test_delete_not_exist_role_entity(
    role_repository: GenericRepository[Roles],
    role_dto: RoleDTO,
):
    with pytest.raises(EntityNotFoundException):
        await role_repository.delete(role_dto.uuididf)
    assert len(await role_repository.get_batch()) == 0


@pytest.mark.asyncio
async def test_create_user_entity(
    user_dto: UserDTO, user_repository: GenericRepository[Users]
):

    entity = await user_repository.save(user_dto)
    assert len(await user_repository.get_batch()) == 1
    assert entity.uuididf == user_dto.uuididf
    assert entity.username == user_dto.username


@pytest.mark.asyncio
async def test_create_user_entity_with_not_exist_role_uuididf(
    user_repository: GenericRepository[Users],
):
    user_dto = UserDTO(uuididf=uuid.uuid4(), username="Jhon", role_uuididf=uuid.uuid4())
    with pytest.raises(ForeignKeyNotExist):
        await user_repository.save(user_dto)
    assert len(await user_repository.get_batch()) == 1


@pytest.mark.asyncio
async def test_update_user_entity_with_not_exist_role_uuididf(
    user_repository: GenericRepository[Users],
    user_dto: UserDTO,
):
    user_dto.role_uuididf = uuid.uuid4()
    with pytest.raises(ForeignKeyNotExist):
        await user_repository.update(user_dto)
    assert len(await user_repository.get_batch()) == 1
