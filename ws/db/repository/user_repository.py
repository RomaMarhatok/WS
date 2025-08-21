from ws.db.models import Users
from ws.dto import UserDTO
from ws.db.repository.base_repository import GenericRepository


class UserRepository(GenericRepository[Users, UserDTO]):
    pass
