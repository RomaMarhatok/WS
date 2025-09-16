from fastapi.exceptions import HTTPException
from fastapi import status


HTTP_404_RECORD_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Records by that criteria doesn't found",
)
