from fastapi.exceptions import HTTPException
from fastapi import status


HTTP_400_INCORRECT_USERNAME_OR_PASSWORD = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Incorrect username or password",
)

HTTP_409_CONFLICT_USERNAME_ALREADY_EXIST = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="This username already exist",
)
