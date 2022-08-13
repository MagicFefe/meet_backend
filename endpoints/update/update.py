from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from starlette.requests import Request
from fastapi.responses import FileResponse
from request_checkers.admin_check_route import AdminRightsRoute
from di.application_container import ApplicationContainer
from config import ANDROID_CLIENT_PLATFORM_NAME, FILE_MEDIA_TYPE_ANDROID
from request_checkers.update_endpoint_request_check import check_client_platform, check_update_file_version, \
    check_content_type, check_update_file_size
from services.update.update_service import UpdateService

router = APIRouter(
    prefix="/api/update",
    tags=["update"],
    route_class=AdminRightsRoute,
    dependencies=[
        Depends(check_client_platform)
    ]
)


@router.post(
    path="/{client_platform}",
    dependencies=[
        Depends(check_content_type), Depends(check_update_file_size)
    ]
)
@inject
async def upload_update(
        request: Request,
        update_service: UpdateService = Depends(Provide[ApplicationContainer.service_container.update_service])
):
    update_file_version = request.headers.get("update-file-version")
    await check_update_file_version(update_file_version)
    update_file_bytes = await request.body()
    client_platform = request.path_params.get("client_platform")
    if client_platform == ANDROID_CLIENT_PLATFORM_NAME:
        await update_service.upload_update_file_android(update_file_bytes, update_file_version)


@router.get(
    path="/{client_platform}",
    response_class=FileResponse
)
@inject
async def receive_update(
        client_platform: str,
        service: UpdateService = Depends(Provide[ApplicationContainer.service_container.update_service])
):
    if client_platform == ANDROID_CLIENT_PLATFORM_NAME:
        file_path = await service.get_update_file_path_android()
        return FileResponse(file_path, media_type=FILE_MEDIA_TYPE_ANDROID)


@router.get(
    path="/{client_platform}/version"
)
@inject
async def get_current_update_version(
        client_platform: str,
        service: UpdateService = Depends(Provide[ApplicationContainer.service_container.update_service])
):
    if client_platform == ANDROID_CLIENT_PLATFORM_NAME:
        current_version = await service.get_current_version_android()
        return current_version
