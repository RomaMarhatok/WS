import jwt
import uuid
from datetime import datetime, timedelta, timezone
from fastapi.responses import JSONResponse
from ws.api.schemas.user import POSTUserSchema
from ws.db.uow.base import BaseUOW
from ws.db.exceptions import EntityNotFoundException
from ws.api.exceptions import (
    HTTP_400_INCORRECT_USERNAME_OR_PASSWORD,
    HTTP_401_REFRESH_TOKEN_EXPIRED,
)
from ws.utils.security import verfiy_password
from ws.config import JWTTokenConfig
from ws.utils.date import (
    parse_datetime_to_gmt_format_str,
    parse_gmt_format_str_to_datetime,
)
from ws.dto import TokenDTO, TokenType


class TokenService:
    def __init__(self):
        self.config = JWTTokenConfig
        self.token_types = TokenType
        self.ACCESS_TOKEN_TIMEDELTA = timedelta(minutes=30)
        self.REFRESH_TOKEN_TIMEDELTA = timedelta(days=1)

    async def decode_token(self, token: str) -> TokenDTO:
        decoded_data = jwt.decode(
            token,
            key=self.config.SECRET_KEY,
            algorithms=[
                self.config.ALGORITHM,
            ],
        )
        return TokenDTO.from_instance(**decoded_data)

    def encode_token(self, **token_payload: dict) -> str:
        to_encode = token_payload.copy()
        return jwt.encode(
            payload=to_encode,
            key=self.config.SECRET_KEY,
            algorithm=self.config.ALGORITHM,
        )

    async def get_expire_date_str_in_utc(
        self, delta: timedelta, start: datetime = None
    ) -> str:
        experation_date = (
            start if start is not None else datetime.now(timezone.utc)
        ) + delta
        return parse_datetime_to_gmt_format_str(experation_date)

    async def is_expire(self, token: str) -> bool:
        token_date = await self.decode_token(token)
        expire_dt = parse_gmt_format_str_to_datetime(token_date.expire)
        return datetime.now(timezone.utc) >= expire_dt

    async def refresh(self, token: str) -> str:
        dto = await self.decode_token(token)
        dto.expire = await self.get_expire_date_str_in_utc(self.ACCESS_TOKEN_TIMEDELTA)
        return await self.encode_token(dto.model_dump())


class AuthService:
    def __init__(self, uow: BaseUOW):
        self.uow = uow
        self.token_service = TokenService()

    async def auth(self, credentials: POSTUserSchema) -> JSONResponse:
        try:
            user_dto = await self.uow.users.get_user(username=credentials.username)
            if not verfiy_password(credentials.password, user_dto.password):
                raise HTTP_400_INCORRECT_USERNAME_OR_PASSWORD
            return await self._get_auth_response(user_dto.uuididf, user_dto.username)
        except EntityNotFoundException:
            raise HTTP_400_INCORRECT_USERNAME_OR_PASSWORD

    async def _get_auth_response(self, uuididf: uuid.UUID, username: str):
        access_token_expire_date = await self.token_service.get_expire_date_str_in_utc(
            self.token_service.ACCESS_TOKEN_TIMEDELTA
        )
        access_token = await self.token_service.encode_token(
            uuididf=uuididf,
            username=username,
            expire=access_token_expire_date,
            type=self.token_service.token_types.ACCESS,
        )
        refresh_token_expire_date = await self.token_service.get_expire_date_str_in_utc(
            self.token_service.REFRESH_TOKEN_TIMEDELTA
        )
        refresh_token = await self.token_service.encode_token(
            uuididf=uuididf,
            username=username,
            expire=refresh_token_expire_date,
            type=self.token_service.token_types.REFRESH,
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
            expires=refresh_token_expire_date,
            secure=True,
            httponly=True,
        )
        return resp

    async def refresh_access_token(
        self, refresh_token: str, access_token: str
    ) -> tuple[str, str]:
        if await self.token_service.is_expire(refresh_token):
            raise HTTP_401_REFRESH_TOKEN_EXPIRED
        access_token = await self.token_service.refresh(access_token)
        return refresh_token, access_token
