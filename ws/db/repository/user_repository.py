from models.users import Users
from ws.api.v1.schemas.user import UserUpdateDTO, UserCreationDTO
from ws.db.repository.generic_repository import GenericRepository


class UserRepository(GenericRepository[Users, UserCreationDTO, UserUpdateDTO]):
    pass
