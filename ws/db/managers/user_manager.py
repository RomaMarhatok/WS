import uuid
from ws.dto import UserDTO
from ws.dto.role import RoleNameEnum
from ws.db import models
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
        (base_user_role_uuididf,) = await self.get_repository(models.Roles).find(
            models.roles.Roles.rolename == RoleNameEnum.BASE_USER,
            selected_fields=(models.Roles.uuididf),
            get_first=True,
            get_flat_result=True,
        )
        dto = UserDTO(
            username=user_data.username,
            password=user_data.password,
            role_uuididf=base_user_role_uuididf,
            uuididf=uuid.uuid4(),
        )
        await self.get_repository(models.Users).save(dto)
