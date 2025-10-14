import uuid
import pytest
from ws.db.models import Roles
from ws.dto import RoleDTO


@pytest.mark.asyncio
@pytest.mark.parametrize("role_uuididf,rolename", [(uuid.uuid4(), "fakerolename")])
async def test_get_dto_from_db_instance(role_uuididf: uuid.UUID, rolename: str):
    role = Roles(uuididf=role_uuididf, rolename=rolename)
    dto = RoleDTO.from_instance(role)
    assert role.uuididf == dto.uuididf
    assert role.rolename == dto.rolename


@pytest.mark.asyncio
async def test_negative_get_dto_from_db_instance():
    role = Roles()
    with pytest.raises(AttributeError):
        RoleDTO.from_instance(role)


@pytest.mark.asyncio
@pytest.mark.parametrize("role_uuididf,rolename", [(uuid.uuid4(), "fakerolename")])
async def test_compare_dto_with_db_instance(role_uuididf: uuid.UUID, rolename: str):
    role = Roles(uuididf=role_uuididf, rolename=rolename)
    dto = RoleDTO.from_instance(role)
    assert dto == role


@pytest.mark.asyncio
@pytest.mark.parametrize("role_uuididf,rolename", [(uuid.uuid4(), "fakerolename")])
async def test_negative_dto_comparation_with_db_instance(
    role_uuididf: uuid.UUID, rolename: str
):
    role = Roles(uuididf=role_uuididf, rolename=rolename)
    dto = RoleDTO(uuididf=uuid.uuid4(), rolename="hello")
    assert not (role == dto)
