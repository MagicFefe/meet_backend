from typing import Optional
from uuid import UUID
from db.enitites.user.user import User
from models.auth.sign_up import SignUp
from models.user.user_update import UserUpdate
from repositories.user.user_repository import UserRepository


class UserService:
    def __init__(
            self,
            repository: UserRepository
    ):
        self.__repository = repository

    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        user = await self.__repository.get_user_by_id(user_id)
        return user

    async def get_user_by_email(self, email: str) -> Optional[User]:
        user = await self.__repository.get_user_by_email(email)
        return user

    async def create_user(self, new_user: SignUp):
        await self.__repository.create_user(new_user)

    async def update_user(self, user: UserUpdate, old_user_email: str):
        updated_user = await self.__repository.update_user(user, old_user_email)
        return updated_user

    async def delete_user(self, user_id: UUID):
        await self.__repository.delete_user(user_id)
