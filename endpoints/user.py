from http import HTTPStatus
from fastapi import Depends, APIRouter, Path, HTTPException
from models.user.user_register import UserRegister
from models.user.user_response import UserResponse
from repositories.user_repository import UserRepository, from_user_to_user_response
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies import get_session, get_user_repository
from exceptions import UserAlreadyExistsError

router = APIRouter()


@router.post(
    path="/api/user",
    status_code=201,
    response_model=UserResponse,
    responses={
        201: {
            "description": "Success",
            "model": UserResponse
        },
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
async def create_user(
        user_register: UserRegister,
        session: AsyncSession = Depends(get_session),
        repository: UserRepository = Depends(get_user_repository)
):
    async with session.begin():
        try:
            await repository.create_user(session, user_register)
        except UserAlreadyExistsError:
            raise HTTPException(status_code=409, detail="user with this email already exists")
    created_user_db = await repository.get_user_by_email(session, user_register.email)
    new_user = from_user_to_user_response(created_user_db)
    return new_user


@router.get(
    path="/api/user/{user_email}",
    status_code=200,
    response_model=UserResponse,
    responses={
        200: {
            "description": "Success",
            "content": {
                "application/json": {
                    "example": 200
                }
            }
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
async def get_user(
        user_email: str = Path("User's email"),
        session: AsyncSession = Depends(get_session),
        user_repository: UserRepository = Depends(get_user_repository)
):
    async with session.begin():
        user = await user_repository.get_user_by_email(session, user_email)
    if user is None:
        raise HTTPException(status_code=404, detail="user with this email does not exists")
    response = from_user_to_user_response(user)
    return response


@router.delete(
    path="/api/user/{user_email}",
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
        user_email: str = Path("User's email"),
        session: AsyncSession = Depends(get_session),
        repository: UserRepository = Depends(get_user_repository)
):
    async with session.begin():
        await repository.delete_user(session, user_email)
    return HTTPStatus.OK
