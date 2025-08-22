import uuid
from fastapi.responses import JSONResponse
from ws.api.exceptions import (
    HTTP_400_INCORRECT_USERNAME_OR_PASSWORD,
    HTTP_409_CONFLICT_USERNAME_ALREADY_EXIST,
)
from ws.api.schemas.user import POSTUserSchema
from ws.db.repository import RoleRepository, UserRepository
from ws.db.session import get_session_factory
from ws.db.exceptions import EntityAlreadyExistException, CouldNotCreateEntityException
from ws.dto import UserDTO
from ws.utils.security import get_password_hash


class RegistrationService:
    def __init__(self):
        self.user_repo = UserRepository(get_session_factory()())
        self.role_repo = RoleRepository(get_session_factory()())

    async def registration(self, credentials: POSTUserSchema) -> JSONResponse:
        try:
            role = await self.role_repo.get_by_name("base_user")
            hashed_password = get_password_hash(credentials.password)
            dto = UserDTO(
                username=credentials.username,
                password=hashed_password,
                role_uuididf=role.uuididf,
                uuididf=uuid.uuid4(),
            )
            await self.user_repo.save(dto)
            return JSONResponse(content={"msg": "User has been created"})
        except EntityAlreadyExistException:
            raise HTTP_409_CONFLICT_USERNAME_ALREADY_EXIST
        except CouldNotCreateEntityException:
            raise HTTP_400_INCORRECT_USERNAME_OR_PASSWORD
