import uuid
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from ws.api.schemas.user import POSTUserSchema
from ws.api.exceptions.auth import HTTP_401_REFRESH_TOKEN_EXPIRED
from ws.api.exceptions.user import HTTP_400_INCORRECT_USERNAME_OR_PASSWORD
from ws.utils.security import verfiy_password
from ws.service.auth.token_service import TokenService
from ws.service.base import BaseService
from ws.db.uow.base import BaseUOW
from ws.db.exceptions import EntityNotFoundException


class AuthService(BaseService):
    def __init__(
        self,
        uow: BaseUOW,
        db_to_http_exception_map: dict[Exception, HTTPException] = {
            EntityNotFoundException: HTTP_400_INCORRECT_USERNAME_OR_PASSWORD,
        },
    ):
        super().__init__(
            db_to_http_exception_map=db_to_http_exception_map,
            uow=uow,
        )
        self.token_service = TokenService()

    async def auth(self, credentials: POSTUserSchema) -> JSONResponse:
        user_dto = await self.uow.users.get_user(username=credentials.username)
        if not verfiy_password(credentials.password, user_dto.password):
            raise HTTP_400_INCORRECT_USERNAME_OR_PASSWORD
        return await self._get_auth_response(user_dto.uuididf)

    async def _get_auth_response(self, uuididf: uuid.UUID):
        access_token = await self.token_service.create_access_token(sub=uuididf)
        refresh_token = await self.token_service.create_refresh_token(
            uuididf=uuididf,
        )
        resp = JSONResponse(
            content={
                "msg": "Authentication successfully",
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "Bearer",
            }
        )
        return resp

    async def refresh_access_token(
        self, refresh_token: str, access_token: str
    ) -> tuple[str, str]:
        if await self.token_service.is_expire(refresh_token):
            raise HTTP_401_REFRESH_TOKEN_EXPIRED
        access_token = await self.token_service.refresh(access_token)
        return refresh_token, access_token
