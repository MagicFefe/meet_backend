from http import HTTPStatus
from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, APIRouter
from starlette import status
from di.application_container import ApplicationContainer
from files.file_manager import FileManager
from models.user.user_response import UserResponseWithToken, UserResponse
from models.user.user_update import UserUpdate
from repositories.user_repository import UserRepository, from_user_to_user_response
from exceptions import InvalidImageError
from uuid import UUID
from utils.password_utils import get_hashed_password
from utils.image_validation import validate_image
from sqlalchemy.orm.exc import UnmappedInstanceError

router = APIRouter(
    prefix="/api/user",
    tags=["user"]
)


@router.get(
    path="/{user_id}",
    status_code=200,
    response_model=UserResponse,
    responses={
        404: {
            "description": "Not found",
            "content": {
                "application/json": {
                    "example": {"description": "user with this email does not exists"}
                }
            }
        }
    }
)
@inject
async def get_user_by_id(
        user_id: str,
        user_repository: UserRepository = Depends(Provide[ApplicationContainer.repository_container.user_repository]),
        user_image_file_manager: FileManager =
        Depends(Provide[ApplicationContainer.file_storage_container.user_image_file_manager])
):
    try:
        user = await user_repository.get_user_by_id(UUID(user_id))
    except Exception:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="bad id")
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user with this id does not exists")
    result = from_user_to_user_response(user, user_image_file_manager)
    return result


@router.put(
    path="",
    status_code=status.HTTP_200_OK,
    response_model=UserResponseWithToken
)
@inject
async def update_user_data(
        user_update: UserUpdate,
        user_repository: UserRepository = Depends(Provide[ApplicationContainer.repository_container.user_repository])
):
    try:
        validate_image(user_update.image)
    except InvalidImageError as error:
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail=error.detail)
    try:
        old_user = await user_repository.get_user_by_id(UUID(user_update.id))
    except Exception:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="invalid user id")
    if old_user.password != get_hashed_password(user_update.old_password, old_user.email):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="incorrect password")
    updated_user = await user_repository.update_user(user_update, old_user.email)
    return updated_user


@router.delete(
    path="/{user_id}",
    response_model=int,
    responses={
        200: {
            "description": "Success",
            "content": {
                "application/json": {
                    "example": 200
                }
            }
        }
    }
)
@inject
async def delete_user(
        user_id: str,
        repository: UserRepository = Depends(Provide[ApplicationContainer.repository_container.user_repository])
):
    try:
        await repository.delete_user(UUID(user_id))
    except UnmappedInstanceError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="bad id")
    return HTTPStatus.OK
