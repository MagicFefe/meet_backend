from typing import Optional, Callable, AsyncIterator
from db.enitites.user.mappers.mappers import from_user_to_user_response_with_token
from exceptions import UserAlreadyExistsError
from sqlalchemy.ext.asyncio import AsyncSession
from models.auth.mappers.mappers import from_sign_up_to_user
from models.auth.sign_up import SignUp
from models.user.user_update import UserUpdate
from db.enitites.user.user import User
from sqlalchemy.future import select
from utils.password_utils import get_hashed_password
from uuid import UUID
from sqlalchemy.sql.expression import update
from files.file_manager import FileManager


class UserRepository:
    def __init__(
            self,
            db_session: Callable[[], AsyncIterator[AsyncSession]],
            user_image_file_manager: FileManager,
    ):
        self.__db_session = db_session
        self.__user_image_file_manager = user_image_file_manager

    async def get_user_by_email(self, email: str) -> Optional[User]:
        async with self.__db_session() as session:
            result = await session.execute(select(User).where(User.email == email))
            return result.scalar_one_or_none()

    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        async with self.__db_session() as session:
            result = await session.execute(select(User).where(User.id == user_id))
            return result.scalar_one_or_none()

    async def get_users_by_ids(self, user_ids: list[UUID]) -> list[User] | None:
        async with self.__db_session() as session:
            users = await session.execute(select(User).where(User.id.in_(user_ids)))
            return users.scalars()

    async def create_user(self, new_user: SignUp):
        async with self.__db_session() as session:
            user_db = await self.get_user_by_email(new_user.email)
            user_not_exists: bool = user_db is None
            if user_not_exists:
                user_db = await from_sign_up_to_user(new_user, self.__user_image_file_manager)
                session.add(user_db)
                await session.commit()
            else:
                raise UserAlreadyExistsError("user already exists, cannot register")

    async def update_user(
            self,
            user: UserUpdate,
            old_user_email: str
    ):
        old_user_image_filename = f"{old_user_email}.txt"
        await self.__user_image_file_manager.delete_file(old_user_image_filename)
        new_user_image_filename = f"{user.email}.txt"
        new_image_filename = await self.__user_image_file_manager.write_or_create_file(
            new_user_image_filename,
            user.image
        )
        async with self.__db_session() as session:
            await session.execute(
                update(User).where(User.id == UUID(user.id)).values(
                    name=user.name,
                    surname=user.surname,
                    about=user.about,
                    dob=user.dob,
                    gender=user.gender,
                    email=user.email,
                    country=user.country,
                    city=user.city,
                    password=get_hashed_password(user.new_password, user.email),
                    image_filename=new_image_filename
                )
            )
            await session.commit()
            new_user_db = await self.get_user_by_id(UUID(user.id))
            new_user = await from_user_to_user_response_with_token(new_user_db, self.__user_image_file_manager)
            return new_user

    # TODO: Implement soft and hard deletion
    async def delete_user(self, user_id: UUID):
        user = await self.get_user_by_id(user_id)
        async with self.__db_session() as session:
            await session.delete(user)
            await session.commit()
