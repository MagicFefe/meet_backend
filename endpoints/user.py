from base64 import b64decode
from io import BytesIO
from http import HTTPStatus
from fastapi import Depends, Path, HTTPException, APIRouter
from models.user.user_register import UserRegister
from models.user.user_response import UserResponse
from models.user.user_minimal import UserMinimal
from repositories.user_repository import UserRepository, from_user_to_user_response
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies import get_session, get_user_repository
from exceptions import UserAlreadyExistsError
from uuid import UUID
from utils.password_utils import get_hashed_password
from config import MIN_USER_IMAGE_WIDTH_PX, MIN_USER_IMAGE_HEIGHT_PX, \
    MAX_USER_IMAGE_WIDTH_PX, MAX_USER_IMAGE_HEIGHT_PX
from PIL import Image

router = APIRouter(
    prefix="/api/user",
    tags=["user"]
)


@router.post(
    path="/sign_up",
    status_code=201,
    response_model=UserResponse,
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
            decoded_image = Image.open(BytesIO(b64decode(user_register.image)))
        except Exception:
            raise HTTPException(status_code=415, detail="image must be jpeg or png format")
        width, height = decoded_image.size
        if width != height:
            raise HTTPException(status_code=415, detail="image must be a square")
        if width < MIN_USER_IMAGE_WIDTH_PX or height < MIN_USER_IMAGE_HEIGHT_PX:
            raise HTTPException(status_code=415, detail="image is too small")
        if width > MAX_USER_IMAGE_WIDTH_PX or MAX_USER_IMAGE_HEIGHT_PX > 1000:
            raise HTTPException(status_code=415, detail="image is to large")
    async with session.begin():
        try:
            await repository.create_user(session, user_register)
        except UserAlreadyExistsError:
            raise HTTPException(status_code=409, detail="user with this email already exists")
    created_user_db = await repository.get_user_by_email(session, user_register.email)
    new_user = from_user_to_user_response(created_user_db)
    return new_user


@router.post(
    path="/sign_in",
    status_code=200,
    response_model=UserResponse,
    responses={
        201: {
            "user": UserResponse
        },
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
        return from_user_to_user_response(user)
    else:
        raise HTTPException(status_code=422, detail="incorrect password")


@router.get(
    path="/{user_id}",
    status_code=200,
    response_model=UserResponse,
    responses={
        200: {
            "user": UserResponse
        },
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
        except:
            raise HTTPException(status_code=422, detail="bad id")
    if user is None:
        raise HTTPException(status_code=404, detail="user with this email does not exists")
    response = from_user_to_user_response(user)
    return response


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
