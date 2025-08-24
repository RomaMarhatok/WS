from fastapi.responses import JSONResponse
from ws.api.exceptions import (
    HTTP_400_INCORRECT_USERNAME_OR_PASSWORD,
    HTTP_409_CONFLICT_USERNAME_ALREADY_EXIST,
)
from ws.api.schemas.user import POSTUserSchema
from ws.db.exceptions import EntityAlreadyExistException, CouldNotCreateEntityException
from ws.db.uow.base import BaseUOW


class RegistrationService:
    def __init__(self, uow: BaseUOW):
        self.uow = uow

    async def registration(self, credentials: POSTUserSchema) -> JSONResponse:
        try:
            await self.uow.users.save_user(credentials)
            return JSONResponse(content={"msg": "User has been created"})
        except EntityAlreadyExistException:
            raise HTTP_409_CONFLICT_USERNAME_ALREADY_EXIST
        except CouldNotCreateEntityException:
            raise HTTP_400_INCORRECT_USERNAME_OR_PASSWORD
