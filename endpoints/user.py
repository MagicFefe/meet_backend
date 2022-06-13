from http import HTTPStatus
from fastapi import Depends, APIRouter, Path
from fastapi.responses import JSONResponse
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
            return JSONResponse(status_code=409, content={"message": "user with this email already exists"})
    created_user_db = await repository.get_user_by_email(session, user_register.email)
    new_user = from_user_to_user_response(created_user_db)
    return new_user


@router.delete(path="/api/user/{user_email}", status_code=200, response_model=int)
async def delete_user(
        user_email: str = Path("User's email"),
        session: AsyncSession = Depends(get_session),
        repository: UserRepository = Depends(get_user_repository)
) -> int:
    async with session.begin():
        await repository.delete_user(session, user_email)
    return HTTPStatus.OK
