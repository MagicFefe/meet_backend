from typing import Optional
from exceptions import UserAlreadyExistsError
from sqlalchemy.ext.asyncio import AsyncSession
from models.user.user_register import UserRegister
from db.enitites.user import User
from models.user.user_response import UserResponse
from sqlalchemy.future import select
from utils.password_utils import get_hashed_password
from utils.jwt_utils import generate_jwt
from uuid import UUID


class UserRepository:
    async def get_user_by_email(self, db_session: AsyncSession, email: str) -> Optional[User]:
        result = await db_session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_user_by_id(self, db_session: AsyncSession, user_id: UUID) -> Optional[User]:
        result = await db_session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def create_user(self, db_session: AsyncSession, new_user: UserRegister):
        async with db_session:
            user_db = await self.get_user_by_email(db_session, new_user.email)
            user_not_exists: bool = user_db is None
            if user_not_exists:
                user_db = from_user_register_to_user(new_user)
                db_session.add(user_db)
                await db_session.commit()
            else:
                raise UserAlreadyExistsError("User already exists, cannot register")

    async def delete_user(self, db_session: AsyncSession, user_id: UUID):
        user = await self.get_user_by_id(db_session, user_id)
        await db_session.delete(user)
        await db_session.commit()


def from_user_register_to_user(user_register: UserRegister) -> User:
    user = User()
    user.name = user_register.name
    user.surname = user_register.surname
    user.email = user_register.email
    user.city = user_register.city
    user.country = user_register.country
    user.password = \
        get_hashed_password(user_register.password, user_register.email, user_register.name, user_register.surname)
    return user


def from_user_to_user_response(user: User):
    jwt = generate_jwt(
        {
            "name": user.name,
            "surname": user.surname,
            "email": user.email
        }
    )
    user_response = UserResponse(
        id=str(user.id),
        name=user.name,
        surname=user.surname,
        email=user.email,
        country=user.country,
        city=user.city,
        jwt=str(jwt)
    )
    return user_response
