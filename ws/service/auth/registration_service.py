from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from ws.api.exceptions.user import (
    HTTP_400_INCORRECT_USERNAME_OR_PASSWORD,
    HTTP_409_CONFLICT_USERNAME_ALREADY_EXIST,
)
from ws.api.schemas.user import POSTUserSchema
from ws.db.exceptions import EntityAlreadyExistException, CouldNotCreateEntityException
from ws.db.uow.base import BaseUOW
from ws.service.base import BaseService


class RegistrationService(BaseService):
    def __init__(
        self,
        uow: BaseUOW,
        db_to_http_exception_map: dict[Exception, HTTPException] = {
            EntityAlreadyExistException: HTTP_409_CONFLICT_USERNAME_ALREADY_EXIST,
            CouldNotCreateEntityException: HTTP_400_INCORRECT_USERNAME_OR_PASSWORD,
        },
    ):
        super().__init__(
            db_to_http_exception_map=db_to_http_exception_map,
            uow=uow,
        )

    async def registration(self, credentials: POSTUserSchema) -> JSONResponse:
        await self.uow.users.save_user(credentials)
        return JSONResponse(content={"msg": "User has been created"})
