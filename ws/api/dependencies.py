from fastapi import Depends
from service.warehouse_service import WarehousesService
from service.auth.auth_service import AuthService
from service.auth.registration_service import RegistrationService
from db.uow.base import BaseUOW
from db.session import get_session_factory
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncSession,
)


def get_base_uow(
    session_factory: async_sessionmaker[AsyncSession] = Depends(get_session_factory),
) -> BaseUOW:
    return BaseUOW(session_factory)


def get_warehouse_serivce(uow: BaseUOW = Depends(get_base_uow)):
    return WarehousesService(uow=uow)


def get_authentication_service(uow: BaseUOW = Depends(get_base_uow)):
    return AuthService(uow=uow)


def get_registration_service(uow: BaseUOW = Depends(get_base_uow)):
    return RegistrationService(uow=uow)
