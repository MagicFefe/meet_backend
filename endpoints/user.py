from http import HTTPStatus
from fastapi import Depends, Path, HTTPException, APIRouter
from models.user.user_register import UserRegister
from models.user.user_response import UserResponseWithToken, UserResponse
from models.user.user_update import UserUpdate
from models.user.user_minimal import UserMinimal
from repositories.user_repository import UserRepository, from_user_to_user_response, \
    from_user_to_user_response_with_token
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies import get_session, get_user_repository
from exceptions import UserAlreadyExistsError, InvalidImageError
from uuid import UUID
from utils.password_utils import get_hashed_password
from utils.image_validation import validate_image

router = APIRouter(
    prefix="/api/user",
    tags=["user"]
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
async def sign_up_user(
        user_register: UserRegister,
        session: AsyncSession = Depends(get_session),
        repository: UserRepository = Depends(get_user_repository)
):
    if not (user_register.image is None):
        try:
            validate_image(user_register.image)
        except InvalidImageError as error:
            raise HTTPException(status_code=415, detail=error.detail)
    async with session.begin():
        try:
            await repository.create_user(session, user_register)
        except UserAlreadyExistsError:
            raise HTTPException(status_code=409, detail="user with this email already exists")
    created_user_db = await repository.get_user_by_email(session, user_register.email)
    return from_user_to_user_response_with_token(created_user_db)


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
async def sign_in_user(
        user_minimal: UserMinimal,
        session: AsyncSession = Depends(get_session),
        repository: UserRepository = Depends(get_user_repository)
):
    user = await repository.get_user_by_email(session, user_minimal.email)
    if user is None:
        raise HTTPException(status_code=404, detail="user does not exist")
    hashed_password = get_hashed_password(user_minimal.password, user_minimal.email)
    if user.password == hashed_password:
        return from_user_to_user_response_with_token(user)
    else:
        raise HTTPException(status_code=422, detail="incorrect password")


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
async def get_user_by_id(
        user_id: str = Path("User's id"),
        session: AsyncSession = Depends(get_session),
        user_repository: UserRepository = Depends(get_user_repository)
):
    async with session.begin():
        try:
            user = await user_repository.get_user_by_id(session, UUID(user_id))
        except Exception:
            raise HTTPException(status_code=422, detail="bad id")
    if user is None:
        raise HTTPException(status_code=404, detail="user with this email does not exists")
    return from_user_to_user_response(user)


@router.put(
    path="",
    status_code=200,
    response_model=UserResponseWithToken
)
async def update_user_data(
        user_update: UserUpdate,
        session: AsyncSession = Depends(get_session),
        user_repository: UserRepository = Depends(get_user_repository)
):
    try:
        validate_image(user_update.image)
    except InvalidImageError as error:
        raise HTTPException(status_code=415, detail=error.detail)
    try:
        old_user = await user_repository.get_user_by_id(session, UUID(user_update.id))
    except Exception:
        raise HTTPException(status_code=422, detail="invalid user id")
    if old_user.password != get_hashed_password(user_update.old_password, user_update.new_email):
        raise HTTPException(status_code=422, detail="incorrect password")
    updated_user = await user_repository.update_user(session, user_update)
    return updated_user


@router.delete(
    path="/{user_id}",
    status_code=200,
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
async def delete_user(
        user_id: str = Path("User's id"),
        session: AsyncSession = Depends(get_session),
        repository: UserRepository = Depends(get_user_repository)
):
    async with session.begin():
        await repository.delete_user(session, UUID(user_id))
    return HTTPStatus.OK
