from ws.dto.base import BaseDTO
from enum import Enum
from typing import Optional


class TokenType(Enum):
    ACCESS = "ACCESS"
    REFRESH = "REFRESH"


class TokenDTO(BaseDTO):
    uuididf: str
    username: Optional[str] = None
    expire: str
    type: TokenType
