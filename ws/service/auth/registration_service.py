from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from ws.api.exceptions.user import (
    HTTP_400_INCORRECT_USERNAME_OR_PASSWORD,
    HTTP_409_CONFLICT_USERNAME_ALREADY_EXIST,
)
from ws.api.schemas.user import POSTUserRequest
from ws.db.repository.exceptions import (
    EntityAlreadyExistException,
    CouldNotCreateEntityException,
)
from ws.db.uow.base import BaseUOW
from ws.service.base import BaseService
from ws.utils.security import get_password_hash


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

    async def registration(self, credentials: POSTUserRequest) -> JSONResponse:
        credentials.password = get_password_hash(credentials.password)
        await self.uow.users.save_user(credentials)
        return JSONResponse(content={"msg": "User has been created"})
