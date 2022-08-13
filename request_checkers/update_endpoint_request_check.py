from dependency_injector.wiring import Provide
from fastapi import Header, HTTPException, Body, Path
from starlette import status
from config import SUPPORTED_UPDATE_FILE_CONTENT_TYPES, MIN_UPDATE_FILE_SIZE_BYTES, MAX_UPDATE_FILE_SIZE_BYTES, \
    SUPPORTED_PLATFORMS
from di.application_container import ApplicationContainer
from services.update.update_service import UpdateService
from utils.version_utils import first_version_is_lower


async def check_update_file_version(
        update_file_version: str,
        service: UpdateService = Provide[ApplicationContainer.service_container.update_service]
):
    if update_file_version is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="bad update file version"
        )
    current_version = await service.get_current_version_android()
    if len(current_version) > 0:
        if not (first_version_is_lower(current_version, update_file_version)):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="uploading version is older than version on server"
            )


async def check_client_platform(
        client_platform: str = Path(alias="client_platform")
):
    if (client_platform is None) or not (client_platform in SUPPORTED_PLATFORMS):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="unsupported client platform")


async def check_content_type(
        content_type: str = Header(alias="content-type")
):
    if (content_type is None) or not (content_type in SUPPORTED_UPDATE_FILE_CONTENT_TYPES):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="unsupported update file content type"
        )


async def check_update_file_size(
        update_file_bytes: bytes = Body()
):
    update_file_bytes_length = len(update_file_bytes)
    if update_file_bytes_length < MIN_UPDATE_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"file is too small (min size is {MIN_UPDATE_FILE_SIZE_BYTES / 1024} Kb)"
        )
    if update_file_bytes_length > MAX_UPDATE_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"file is too big (max size is {MAX_UPDATE_FILE_SIZE_BYTES / 1024} Mb)"
        )
