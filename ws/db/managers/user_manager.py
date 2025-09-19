import uuid
from ws.dto import UserDTO
from ws.db.models import Users, Roles
from ws.db.managers.manager import BaseManager
from ws.api.schemas import POSTUserRequest


class UserManager(BaseManager):
    """
    Base commands for User model
    Methods:
        async def save_user(self, username: str, password: str) -> None:
            Save a user with role "base_user" in db.
            Password hashed before saving
        async def get_user(selfm**kwargs) -> UserDTO:
            Retrieves a user mathing the given criteria and returns UserDTO instance
    """

    async def save_user(self, user_data: POSTUserRequest) -> None:
        base_user_role: Roles = await self.get_repository(Roles).get(
            rolename="base_user"
        )
        dto = UserDTO(
            username=user_data.username,
            password=user_data.password,
            role_uuididf=base_user_role.uuididf,
            uuididf=uuid.uuid4(),
        )
        await self.get_repository(Users).save(dto)

    async def get_user(self, **kwargs) -> UserDTO:
        user: Users = await self.get_repository(Users).get(**kwargs)
        return UserDTO.from_instance(user)
