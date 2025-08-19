import pytest
import uuid
from pydantic import BaseModel
from ws.test.test_repository.fake_db.fake_tables import FakeAnimalTable, FakeOwnerTable
from ws.db.repository.base_repository import GenericRepository


class AnimalDTO(BaseModel):
    uuididf: uuid.UUID
    animal_name: str


class OwnerDTO(BaseModel):
    uuididf: uuid.UUID
    owner_name: str
    animal_uuidfidf: uuid.UUID


@pytest.fixture(scope="session")
def animal_repository(async_session_maker_for_test):
    class AnimalRepository(GenericRepository[FakeAnimalTable, AnimalDTO]):
        @property
        def _model(self):
            return FakeAnimalTable

    return AnimalRepository(async_session_maker_for_test)


@pytest.fixture(scope="session")
def owner_repository(async_session_maker_for_test):
    class OwnerRepository(GenericRepository[FakeOwnerTable, OwnerDTO]):
        @property
        def _model(self):
            return FakeOwnerTable

    return OwnerRepository(async_session_maker_for_test)


@pytest.fixture(scope="session")
def animal_dto() -> AnimalDTO:
    return AnimalDTO(uuididf=uuid.uuid4(), animal_name="boby")


@pytest.fixture(scope="session")
def onwer_dto(animal_dto: AnimalDTO) -> OwnerDTO:
    return OwnerDTO(
        uuidf=uuid.uuid4(), owner_name="Tom", animal_uuidfidf=animal_dto.uuididf
    )


@pytest.mark.asyncio
async def test_create_animal_entity(
    migrate_fake_migrations,
    animal_repository: GenericRepository[FakeAnimalTable, AnimalDTO],
    animal_dto: AnimalDTO,
):
    entity = await animal_repository.save(animal_dto)
    assert len(await animal_repository.get_batch()) == 1
    assert entity.uuididf == animal_dto.uuididf
    assert entity.animal_name == animal_dto.animal_name
