from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, APIRouter
from starlette import status
from di.application_container import ApplicationContainer
from exceptions import InvalidImageError, UserAlreadyExistsError
from files.file_manager import FileManager
from models.auth.sign_in import SignIn
from models.auth.sign_up import SignUp
from models.user.user_response import UserResponseWithToken
from repositories.user_repository import UserRepository, from_user_to_user_response_with_token
from utils.image_validation import validate_image
from utils.password_utils import get_hashed_password

router = APIRouter(
    prefix="/api/auth",
    tags=["auth"]
)


@router.post(
    path="/sign_up",
    status_code=201,
    response_model=UserResponseWithToken,
    responses={
        409: {
            "description": "Conflict",
            "content": {
                "application/json": {
                    "example": {"description": "user with this email already exists"}
                }
            }
        }
    }
)
@inject
async def sign_up(
        sign_up_model: SignUp,
        repository: UserRepository = Depends(Provide[ApplicationContainer.repository_container.user_repository]),
        user_image_file_manager: FileManager =
        Depends(Provide[ApplicationContainer.file_storage_container.user_image_file_manager])
):
    if not (sign_up_model.image is None):
        try:
            validate_image(sign_up_model.image)
        except InvalidImageError as error:
            raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail=error.detail)
    try:
        await repository.create_user(sign_up_model)
    except UserAlreadyExistsError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user with this email already exists")
    created_user_db = await repository.get_user_by_email(sign_up_model.email)
    return from_user_to_user_response_with_token(created_user_db, user_image_file_manager)


@router.post(
    path="/sign_in",
    status_code=200,
    response_model=UserResponseWithToken,
    responses={
        404: {
            "detail": "user does not exist"
        },
        422: {
            "detail": "incorrect password"
        }
    }
)
@inject
async def sign_in(
        sign_in_model: SignIn,
        repository: UserRepository = Depends(Provide[ApplicationContainer.repository_container.user_repository]),
        user_image_file_manager: FileManager =
        Depends(Provide[ApplicationContainer.file_storage_container.user_image_file_manager])
):
    user = await repository.get_user_by_email(sign_in_model.email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user does not exist")
    hashed_password = get_hashed_password(sign_in_model.password, sign_in_model.email)
    if user.password == hashed_password:
        return from_user_to_user_response_with_token(user, user_image_file_manager)
    else:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="incorrect password")
