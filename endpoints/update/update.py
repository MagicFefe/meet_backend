from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, HTTPException, Depends
from starlette import status
from starlette.requests import Request
from fastapi.responses import FileResponse
from custom_route.admin_check_route import AdminRightsRoute
from di.application_container import ApplicationContainer
from files.file_manager import FileManager
from config import SUPPORTED_UPDATE_FILE_CONTENT_TYPES, SUPPORTED_PLATFORMS, MIN_UPDATE_FILE_SIZE, \
    ANDROID_CLIENT_PLATFORM_NAME, FILE_MEDIA_TYPE_ANDROID, ANDROID_UPDATE_FILENAME, \
    CURRENT_VERSION_UPDATE_FILE_FILENAME, ADMIN_SECRET
from utils.version_utils import first_version_is_lower

router = APIRouter(
    prefix="/api/update",
    tags=["update"],
    route_class=AdminRightsRoute
)


@router.post(
    path="/{client_platform}",
)
@inject
async def upload_update(
        request: Request,
        update_file_file_manager_android: FileManager = Depends(
            Provide[ApplicationContainer.file_storage_container.update_file_file_manager_android]
        )
):
    admin_secret = request.headers.get("admin-secret", None)
    if (admin_secret is None) or not (admin_secret == ADMIN_SECRET):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="you do not have admin rights")
    client_platform = request.path_params.get("client_platform", None)
    if (client_platform is None) or not (client_platform in SUPPORTED_PLATFORMS):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="unsupported client platform")
    content_type = request.headers.get("content-type", None)
    if (content_type is None) or not (content_type in SUPPORTED_UPDATE_FILE_CONTENT_TYPES):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="unsupported update file content type"
        )
    update_file_bytes = await request.body()
    if len(update_file_bytes) < MIN_UPDATE_FILE_SIZE:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="file is too small")
    if client_platform == ANDROID_CLIENT_PLATFORM_NAME:
        update_file_version: str | None = request.headers.get("update-file-version", None)
        if not (update_file_version is None):
            try:
                current_version = update_file_file_manager_android.read_file(CURRENT_VERSION_UPDATE_FILE_FILENAME)
                if first_version_is_lower(current_version, update_file_version):
                    update_file_file_manager_android.rewrite_file_bytes(ANDROID_UPDATE_FILENAME, update_file_bytes)
                    update_file_file_manager_android.rewrite_file(CURRENT_VERSION_UPDATE_FILE_FILENAME,
                                                                  update_file_version)
                    return status.HTTP_200_OK
                else:
                    raise HTTPException(
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        detail="uploading version is older than version on server"
                    )
            except FileNotFoundError:
                update_file_file_manager_android.write_or_create_file_bytes(ANDROID_UPDATE_FILENAME, update_file_bytes)
                update_file_file_manager_android.write_or_create_file(CURRENT_VERSION_UPDATE_FILE_FILENAME,
                                                                      update_file_version)
                return status.HTTP_200_OK
        else:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="bad update file version"
            )


@router.get(
    path="/{client_platform}",
    response_class=FileResponse
)
@inject
async def receive_update(
        client_platform: str,
        update_file_file_manger_android: FileManager =
        Depends(Provide[ApplicationContainer.file_storage_container.update_file_file_manager_android])
):
    if (client_platform is None) or not (client_platform in SUPPORTED_PLATFORMS):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="unsupported client platform")
    if client_platform == ANDROID_CLIENT_PLATFORM_NAME:
        file_path = update_file_file_manger_android.full_storage_path + ANDROID_UPDATE_FILENAME
        return FileResponse(file_path, media_type=FILE_MEDIA_TYPE_ANDROID)


@router.get(
    path="/{client_platform}/version"
)
@inject
async def get_current_update_version(
        client_platform: str,
        update_file_file_manager_android: FileManager =
        Depends(Provide[ApplicationContainer.file_storage_container.update_file_file_manager_android])
):
    if (client_platform is None) or not (client_platform in SUPPORTED_PLATFORMS):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="unsupported client platform")
    if client_platform == ANDROID_CLIENT_PLATFORM_NAME:
        return update_file_file_manager_android.read_file(CURRENT_VERSION_UPDATE_FILE_FILENAME)
