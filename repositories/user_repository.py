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
from config import USER_IMAGE_PLACEHOLDER_PATH, ENCODING, USER_IMAGE_FILE_STORAGE_PATH
from sqlalchemy.sql.expression import update
from files.file_manager import FileManager


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
                raise UserAlreadyExistsError("user already exists, cannot register")

    async def update_user(
            self,
            db_session: AsyncSession,
            user: UserUpdate,
            file_manager: FileManager = FileManager(USER_IMAGE_FILE_STORAGE_PATH)
    ):
        old_user_image_file_name = f"{user.old_email}.txt"
        file_manager.delete_file(old_user_image_file_name)
        new_user_image_file_name = f"{user.new_email}.txt"
        new_image_path = file_manager.write_or_create_file(new_user_image_file_name, user.image)
        async with db_session:
            await db_session.execute(
                update(User).where(User.id == UUID(user.id)).values(
                    name=user.name,
                    surname=user.surname,
                    email=user.new_email,
                    country=user.country,
                    city=user.city,
                    password=get_hashed_password(user.new_password, user.new_email),
                    image_path=new_image_path
                )
            )
            await db_session.commit()
        new_user_db = await self.get_user_by_id(db_session, UUID(user.id))
        new_user = from_user_to_user_response_with_token(new_user_db)
        return new_user

    async def delete_user(self, db_session: AsyncSession, user_id: UUID):
        user = await self.get_user_by_id(db_session, user_id)
        await db_session.delete(user)
        await db_session.commit()


def from_user_register_to_user(
        user_register: UserRegister,
        image_file_manager: FileManager = FileManager(USER_IMAGE_FILE_STORAGE_PATH)
) -> User:
    image_file_name = f"{user_register.email}.txt"
    user = User()
    user.name = user_register.name
    user.surname = user_register.surname
    user.email = user_register.email
    user.city = user_register.city
    user.country = user_register.country
    user.password = \
        get_hashed_password(user_register.password, user_register.email)

    if user_register.image is None:
        with open(USER_IMAGE_PLACEHOLDER_PATH, "rb") as image_file:
            image = b64encode(image_file.read()).decode(ENCODING)
        user.image_path = image_file_manager.write_or_create_file(image_file_name, image)
    else:
        image = user_register.image
        user.image_path = image_file_manager.write_or_create_file(image_file_name, image)
    return user


def from_user_to_user_response_with_token(
        user: User,
        image_file_manager: FileManager = FileManager(USER_IMAGE_FILE_STORAGE_PATH)
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
        email=user.email,
        country=user.country,
        city=user.city,
        jwt=str(jwt),
        image=image_file_manager.read_file(user.image_path)
    )
    return user_response


def from_user_to_user_response(
        user: User,
        image_file_manager: FileManager = FileManager(USER_IMAGE_FILE_STORAGE_PATH)
):
    user_response = UserResponse(
        id=str(user.id),
        name=user.name,
        surname=user.surname,
        email=user.email,
        country=user.country,
        city=user.city,
        image=image_file_manager.read_file(user.image_path)
    )
    return user_response
