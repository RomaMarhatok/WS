import pytest
import uuid
import pytest_asyncio
from pydantic import BaseModel
from ws.test.test_repository.fake_db.fake_tables import FakeAnimalTable, FakeOwnerTable
from ws.db.repository.base_repository import GenericRepository
from ws.db.exceptions import (
    EntityAlreadyExistException,
    EntityNotFoundException,
    ForeignKeyNotExist,
)


class AnimalDTO(BaseModel):
    uuididf: uuid.UUID
    animal_name: str


class OwnerDTO(BaseModel):
    uuididf: uuid.UUID
    owner_name: str
    animal_uuidfidf: uuid.UUID


@pytest.fixture(scope="session")
def animal_repository(async_session_maker_for_test):
    class AnimalRepository(GenericRepository[FakeAnimalTable]):
        pass

    return AnimalRepository(async_session_maker_for_test())


@pytest.fixture(scope="session")
def owner_repository(async_session_maker_for_test):
    class OwnerRepository(GenericRepository[FakeOwnerTable]):
        pass

    return OwnerRepository(async_session_maker_for_test())


@pytest.fixture(scope="session")
def animal_dto() -> AnimalDTO:
    return AnimalDTO(uuididf=uuid.uuid4(), animal_name="boby")


@pytest_asyncio.fixture(scope="session")
async def animal_db(
    animal_repository: GenericRepository[FakeAnimalTable],
    animal_dto: AnimalDTO,
) -> FakeAnimalTable:
    return await animal_repository.save(animal_dto)


@pytest.fixture(scope="session")
def owner_dto(animal_db: FakeAnimalTable) -> OwnerDTO:
    return OwnerDTO(
        uuididf=uuid.uuid4(), owner_name="Tom", animal_uuidfidf=animal_db.uuididf
    )


@pytest.mark.asyncio
async def test_create_animal_entity(
    migrate_fake_migrations,
    animal_repository: GenericRepository[FakeAnimalTable],
    animal_dto: AnimalDTO,
):
    entity = await animal_repository.save(animal_dto)
    assert len(await animal_repository.get_batch()) == 1
    assert entity.uuididf == animal_dto.uuididf
    assert entity.animal_name == animal_dto.animal_name


@pytest.mark.asyncio
async def test_create_already_exist_animal_entity(
    animal_repository: GenericRepository[FakeAnimalTable],
    animal_dto: AnimalDTO,
):
    with pytest.raises(EntityAlreadyExistException):
        await animal_repository.save(animal_dto)


@pytest.mark.asyncio
async def test_get_animal_by_uuididf(
    animal_repository: GenericRepository[FakeAnimalTable],
    animal_dto: AnimalDTO,
):
    entity = await animal_repository.get(uuididf=animal_dto.uuididf)
    assert entity.uuididf == animal_dto.uuididf
    assert entity.animal_name == animal_dto.animal_name


@pytest.mark.asyncio
async def test_get_animal_by_name(
    animal_repository: GenericRepository[FakeAnimalTable],
    animal_dto: AnimalDTO,
):
    entity = await animal_repository.get(animal_name=animal_dto.animal_name)
    assert entity.uuididf == animal_dto.uuididf
    assert entity.animal_name == animal_dto.animal_name


@pytest.mark.asyncio
async def test_get_animal_by_name_with_field(
    animal_repository: GenericRepository[FakeAnimalTable],
    animal_dto: AnimalDTO,
):

    entity = await animal_repository.get(animal_name=animal_dto.animal_name)
    assert entity.uuididf == animal_dto.uuididf
    assert entity.animal_name == animal_dto.animal_name


@pytest.mark.asyncio
async def test_get_not_exist_animal_by_uuididf(
    animal_repository: GenericRepository[FakeAnimalTable],
):
    with pytest.raises(EntityNotFoundException):
        await animal_repository.get(uuididf=uuid.uuid4())


@pytest.mark.asyncio
async def test_get_not_exist_animal_by_name(
    animal_repository: GenericRepository[FakeAnimalTable],
):
    with pytest.raises(EntityNotFoundException):
        await animal_repository.get(animal_name="Cat")


@pytest.mark.asyncio
async def test_multiply_kwarg_in_get_method(
    animal_repository: GenericRepository[FakeAnimalTable],
):
    with pytest.raises(ValueError):
        await animal_repository.get(animal_name="Cat", uuididf=uuid.uuid4())


@pytest.mark.asyncio
async def test_get_animal_by_not_exist_field(
    animal_repository: GenericRepository[FakeAnimalTable],
):
    with pytest.raises(AttributeError):
        await animal_repository.get(not_exist_field="Cat")


@pytest.mark.asyncio
async def test_find_animal_use_find_method(
    animal_repository: GenericRepository[FakeAnimalTable],
    animal_dto: AnimalDTO,
):
    entities = await animal_repository.find(
        animal_name=animal_dto.animal_name, uuididf=animal_dto.uuididf
    )
    assert len(entities) != 0
    assert entities[0].uuididf == animal_dto.uuididf
    assert entities[0].animal_name == animal_dto.animal_name


@pytest.mark.asyncio
async def test_find_animal_with_not_exist_fields_method(
    animal_repository: GenericRepository[FakeAnimalTable],
    animal_dto: AnimalDTO,
):
    with pytest.raises(AttributeError):
        await animal_repository.find(
            not_exist_field=animal_dto.animal_name, uuididf=animal_dto.uuididf
        )


@pytest.mark.asyncio
async def test_find_animal_without_argument(
    animal_repository: GenericRepository[FakeAnimalTable],
):
    with pytest.raises(AttributeError):
        await animal_repository.find()


@pytest.mark.asyncio
async def test_update_animal(
    animal_repository: GenericRepository[FakeAnimalTable],
    animal_dto: AnimalDTO,
):
    animal_dto.animal_name = "foxy"
    entity = await animal_repository.update(animal_dto)
    assert entity.uuididf == animal_dto.uuididf
    assert entity.animal_name == animal_dto.animal_name


@pytest.mark.asyncio
async def test_update_not_exist_entity(
    animal_repository: GenericRepository[FakeAnimalTable],
):
    animal_dto = AnimalDTO(uuididf=uuid.uuid4(), animal_name="boby")
    with pytest.raises(EntityNotFoundException):
        await animal_repository.update(animal_dto)


@pytest.mark.asyncio
async def test_delete_animal_entity(
    animal_repository: GenericRepository[FakeAnimalTable],
    animal_dto: AnimalDTO,
):

    await animal_repository.delete(animal_dto.uuididf)
    assert len(await animal_repository.get_batch()) == 0


@pytest.mark.asyncio
async def test_delete_not_exist_animal_entity(
    animal_repository: GenericRepository[FakeAnimalTable],
    animal_dto: AnimalDTO,
):
    with pytest.raises(EntityNotFoundException):
        await animal_repository.delete(animal_dto.uuididf)
    assert len(await animal_repository.get_batch()) == 0


@pytest.mark.asyncio
async def test_create_owner_entity(
    owner_dto: OwnerDTO, owner_repository: GenericRepository[FakeOwnerTable]
):

    entity = await owner_repository.save(owner_dto)
    assert len(await owner_repository.get_batch()) == 1
    assert entity.uuididf == owner_dto.uuididf
    assert entity.owner_name == owner_dto.owner_name


@pytest.mark.asyncio
async def test_create_owner_entity_with_not_exist_animal_uuididf(
    owner_repository: GenericRepository[FakeOwnerTable],
):
    owner_dto = OwnerDTO(
        uuididf=uuid.uuid4(), owner_name="Jhon", animal_uuidfidf=uuid.uuid4()
    )
    with pytest.raises(ForeignKeyNotExist):
        await owner_repository.save(owner_dto)
    assert len(await owner_repository.get_batch()) == 1


@pytest.mark.asyncio
async def test_update_owner_entity_with_not_exist_animal_uuididf(
    owner_repository: GenericRepository[FakeOwnerTable],
    owner_dto: OwnerDTO,
):
    owner_dto.animal_uuidfidf = uuid.uuid4()
    with pytest.raises(ForeignKeyNotExist):
        await owner_repository.update(owner_dto)
    assert len(await owner_repository.get_batch()) == 1
