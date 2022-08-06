from typing import Optional
from exceptions import UserAlreadyExistsError
from sqlalchemy.ext.asyncio import AsyncSession
from models.user.user_register import UserRegister
from models.user.user_update import UserUpdate
from db.enitites.user import User
from models.user.user_response import UserResponseWithToken, UserResponse
from sqlalchemy.future import select
from utils.password_utils import get_hashed_password
from utils.jwt_utils import generate_jwt
from uuid import UUID
from base64 import b64encode
from config import USER_IMAGE_PLACEHOLDER_PATH, ENCODING
from sqlalchemy.sql.expression import update
from files.file_manager import FileManager


class UserRepository:
    def __init__(
            self,
            user_db_session: AsyncSession,
            user_image_file_manager: FileManager
    ):
        self.__user_db_session = user_db_session
        self.__user_image_file_manager = user_image_file_manager

    async def get_user_by_email(self, email: str) -> Optional[User]:
        result = await self.__user_db_session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        result = await self.__user_db_session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def create_user(self, new_user: UserRegister):
        async with self.__user_db_session.begin():
            user_db = await self.get_user_by_email(new_user.email)
            user_not_exists: bool = user_db is None
            if user_not_exists:
                user_db = from_user_register_to_user(new_user, self.__user_image_file_manager)
                self.__user_db_session.add(user_db)
                await self.__user_db_session.commit()
            else:
                raise UserAlreadyExistsError("user already exists, cannot register")

    async def update_user(
            self,
            user: UserUpdate,
            old_user_email: str
    ):
        old_user_image_filename = f"{old_user_email}.txt"
        self.__user_image_file_manager.delete_file(old_user_image_filename)
        new_user_image_filename = f"{user.email}.txt"
        new_image_filename = self.__user_image_file_manager.write_or_create_file(new_user_image_filename, user.image)
        async with self.__user_db_session.begin():
            await self.__user_db_session.execute(
                update(User).where(User.id == UUID(user.id)).values(
                    name=user.name,
                    surname=user.surname,
                    about=user.about,
                    dob=user.dob,
                    email=user.email,
                    country=user.country,
                    city=user.city,
                    password=get_hashed_password(user.new_password, user.email),
                    image_filename=new_image_filename
                )
            )
            await self.__user_db_session.commit()
        new_user_db = await self.get_user_by_id(UUID(user.id))
        new_user = from_user_to_user_response_with_token(new_user_db, self.__user_image_file_manager)
        return new_user

    async def delete_user(self, user_id: UUID):
        user = await self.get_user_by_id(user_id)
        await self.__user_db_session.delete(user)
        await self.__user_db_session.commit()


def from_user_register_to_user(
        user_register: UserRegister,
        user_image_file_manager: FileManager
) -> User:
    image_file_name = f"{user_register.email}.txt"
    user = User()
    user.name = user_register.name
    user.surname = user_register.surname
    user.dob = user_register.dob
    user.about = user_register.about
    user.email = user_register.email
    user.city = user_register.city
    user.country = user_register.country
    user.password = \
        get_hashed_password(user_register.password, user_register.email)

    if user_register.image is None:
        with open(USER_IMAGE_PLACEHOLDER_PATH, "rb") as image_file:
            image = b64encode(image_file.read()).decode(ENCODING)
        user.image_filename = user_image_file_manager.write_or_create_file(image_file_name, image)
    else:
        image = user_register.image
        user.image_filename = user_image_file_manager.write_or_create_file(image_file_name, image)
    return user


def from_user_to_user_response_with_token(
        user: User,
        user_image_file_manager: FileManager
):
    jwt = generate_jwt(
        {
            "name": user.name,
            "surname": user.surname,
            "email": user.email
        }
    )
    user_response = UserResponseWithToken(
        id=str(user.id),
        name=user.name,
        surname=user.surname,
        about=user.about,
        dob=user.dob,
        email=user.email,
        country=user.country,
        city=user.city,
        jwt=str(jwt),
        image=user_image_file_manager.read_file(user.image_filename)
    )
    return user_response


def from_user_to_user_response(
        user: User,
        user_image_file_manager: FileManager
):
    user_response = UserResponse(
        id=str(user.id),
        name=user.name,
        surname=user.surname,
        about=user.about,
        dob=user.dob,
        email=user.email,
        country=user.country,
        city=user.city,
        image=user_image_file_manager.read_file(user.image_filename)
    )
    return user_response
