from fastapi.exceptions import HTTPException
from fastapi import status


HTTP_401_REFRESH_TOKEN_EXPIRED = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Refresh token expired",
)
