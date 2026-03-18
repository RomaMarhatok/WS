from fastapi import status


class BaseError(Exception):
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    ) -> None:
        self.message = message
        self.status_code = status_code

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self.message}"


class UniqueError(BaseError):
    def __init__(self, model_name: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            message=f"Поля переданные в модель {model_name} содержат "
            "неуникальные значения!",
        )


class NotFoundError(BaseError):
    def __init__(self, message):
        super().__init__(message=message, status_code=status.HTTP_404_NOT_FOUND)


class DatabaseError(BaseError):
    def __init__(self, message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR):
        super().__init__(message, status_code)


class ConflictError(BaseError):
    def __init__(self, message, status_code=status.HTTP_409_CONFLICT):
        super().__init__(message, status_code)
