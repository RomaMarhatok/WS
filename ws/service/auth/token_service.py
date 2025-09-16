import jwt
from datetime import datetime, timedelta, timezone
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

    async def decode_token(self, token: str) -> TokenDTO:
        decoded_data = jwt.decode(
            token,
            key=self.config.SECRET_KEY,
            algorithms=[
                self.config.ALGORITHM,
            ],
        )
        return TokenDTO.from_instance(**decoded_data)

    def _encode_token(self, **token_payload: dict) -> str:
        to_encode = token_payload.copy()
        return jwt.encode(
            payload=to_encode,
            key=self.config.SECRET_KEY,
            algorithm=self.config.ALGORITHM,
        )

    def create_access_token(self, token_payload: dict) -> str:
        data = {"type": self.token_types.ACCESS}
        access_token_expire_date = self.get_expire_date_str_in_utc(
            self.config.ACCESS_TOKEN_TIMEDELTA
        )
        data.update({"expire": access_token_expire_date})
        data.update(**token_payload)

        return self._encode_token(token_payload=token_payload)

    def create_refresh_token(self, token_payload: dict) -> str:
        data = {"type": self.token_types.REFRESH}
        access_token_expire_date = self.get_expire_date_str_in_utc(
            self.config.REFRESH_TOKEN_TIMEDELTA
        )
        data.update({"expire": access_token_expire_date})
        data.update(**token_payload)

        return self._encode_token(token_payload=token_payload)

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
        dto.expire = await self.get_expire_date_str_in_utc(
            self.config.ACCESS_TOKEN_TIMEDELTA
        )
        return await self._encode_token(dto.model_dump())
