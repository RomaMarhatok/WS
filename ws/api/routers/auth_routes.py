from fastapi import APIRouter, Depends
from ws.api.schemas.user import POSTUserSchema
from ws.api.dependencies import (
    get_authentication_service,
    get_registration_service,
)
from ws.service.auth.auth_service import AuthService
from ws.service.auth.registration_service import RegistrationService

auth_router = APIRouter(prefix="auth/")


@auth_router.post("registry/")
async def user_registrastion(
    request: POSTUserSchema,
    service: RegistrationService = Depends(get_registration_service),
):
    return await service.registration(request)


@auth_router.post("authentication/")
async def user_authentication(
    request: POSTUserSchema, service: AuthService = Depends(get_authentication_service)
):
    return await service.auth(request)
