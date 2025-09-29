import pytest
from ws.db.repository.reflectors.fk_reflector import FkReflector


@pytest.fixture(scope="session")
def refl(db_session_factory):
    return FkReflector(db_session_factory)


@pytest.mark.asyncio
async def test_fk_reflection(refl: FkReflector):
    refl = await refl.get_fks_reflection()
    print(refl)


def test_graph():
    from ws.db.models import Items

    print(Items.get_relationships_graph())
