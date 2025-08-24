import jwt
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
from ws.api.schemas.user import POSTUserSchema
from ws.db.uow.base import BaseUOW
from ws.db.exceptions import EntityNotFoundException
from ws.api.exceptions import HTTP_400_INCORRECT_USERNAME_OR_PASSWORD
from ws.utils.security import verfiy_password
from ws.config import JWTTokenConfig
from ws.utils.date import parse_datetime_to_gmt_format_str


class AuthService:
    def __init__(self, uow: BaseUOW):
        self.uow = uow

    async def auth(self, credentials: POSTUserSchema) -> JSONResponse:
        try:
            user_dto = await self.uow.users.get_user(credentials)
            if not verfiy_password(credentials.password, user_dto.password):
                raise HTTP_400_INCORRECT_USERNAME_OR_PASSWORD
            access_token = await self._generate_token(
                {
                    "uuid": str(user_dto.uuididf),
                    "username": user_dto.username,
                    "expire": parse_datetime_to_gmt_format_str(
                        datetime.now() + timedelta(minutes=30)
                    ),
                    "type": "access",
                }
            )
            refresh_token = await self._generate_token(
                {
                    "uuid": str(user_dto.uuididf),
                    "username": user_dto.username,
                    "expire": parse_datetime_to_gmt_format_str(
                        datetime.now() + timedelta(days=1)
                    ),
                    "token_type": "refresh",
                }
            )
            resp = JSONResponse(
                content={
                    "msg": "Authentication successfully",
                    "access_token": access_token,
                }
            )
            resp.set_cookie(
                "refresh_token",
                value=refresh_token,
                expires=parse_datetime_to_gmt_format_str(
                    datetime.now() + timedelta(days=1)
                ),
                secure=True,
                httponly=True,
            )
            return resp
        except EntityNotFoundException:
            raise HTTP_400_INCORRECT_USERNAME_OR_PASSWORD

    async def _generate_token(self, data: dict):
        to_encode = data.copy()

        return jwt.encode(
            payload=to_encode,
            key=JWTTokenConfig.SECRET_KEY,
            algorithm=JWTTokenConfig.ALGORITHM,
        )
