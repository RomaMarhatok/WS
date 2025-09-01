from fastapi.exceptions import HTTPException
from fastapi import status

HTTP_400_INCORRECT_USERNAME_OR_PASSWORD = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST
)
HTTP_409_CONFLICT_USERNAME_ALREADY_EXIST = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="This username already exist",
)
HTTP_401_REFRESH_TOKEN_EXPIRED = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Refresh token expired",
)
HTTP_404_RECORD_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Records by that criteria doesn't found",
)
