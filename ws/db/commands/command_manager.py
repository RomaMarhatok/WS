import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from ws.api.schemas.user import POSTUserSchema
from ws.dto import UserDTO
from ws.utils.security import get_password_hash
from ws.db.repository import GenericRepository
from ws.db.models import Users, Roles
from ws.db.types import SQLALCHEMY_MODEL_TYPE


class UserCommandsManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    def get_repository(
        self, model: SQLALCHEMY_MODEL_TYPE
    ) -> GenericRepository[SQLALCHEMY_MODEL_TYPE]:
        class Repository(GenericRepository[model]):
            pass

        return Repository(self.session)

    async def save_user(self, user_schema: POSTUserSchema) -> None:
        try:
            base_user_role: Roles = await self.get_repository(Roles).get(
                rolename="base_user"
            )
            hashed_password = get_password_hash(user_schema.password)
            dto = UserDTO(
                username=user_schema.username,
                password=hashed_password,
                role_uuididf=base_user_role.uuididf,
                uuididf=uuid.uuid4(),
            )
            await self.get_repository(Users).save(dto)
        except Exception as e:
            raise e

    async def get_user(self, user_schema: POSTUserSchema) -> UserDTO:
        try:

            user: Users = await self.get_repository(Users).get(
                username=user_schema.username
            )
            user.password
            dto = UserDTO(
                username=user.username,
                password=user.password,
                role_uuididf=user.role_uuididf,
                uuididf=uuid.uuid4(),
            )
            return dto
        except Exception as e:
            raise e
