from typing import Optional
from exceptions import UserAlreadyExistsError
from sqlalchemy.ext.asyncio import AsyncSession
from models.user.user_register import UserRegister
from db.enitites.user import User
from models.user.user_response import UserResponse
from sqlalchemy.future import select


class UserRepository:
    async def get_user_by_email(self, db_session: AsyncSession, email: str) -> Optional[User]:
        result = await db_session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_user_by_id(self, db_session: AsyncSession, user_id: int) -> Optional[User]:
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

    async def delete_user(self, db_session: AsyncSession, user_email: str):
        user = await self.get_user_by_email(db_session, user_email)
        await db_session.delete(user)
        await db_session.commit()


def from_user_register_to_user(user_register: UserRegister) -> User:
    user = User()
    user.name = user_register.name
    user.surname = user_register.surname
    user.email = user_register.email
    user.city = user_register.city
    user.country = user_register.country
    user.password = user_register.password
    return user


def from_user_to_user_response(user: User):
    # TODO: add jwt token generation
    user_response = UserResponse(
        name=user.name,
        surname=user.surname,
        email=user.email,
        country=user.country,
        city=user.city,
        jwt=""
    )
    return user_response
