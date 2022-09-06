from datetime import datetime
from uuid import UUID

from db.enitites.chat.chat import Chat
from models.chat.chat_create import ChatCreate
from repositories.chat.chat_repository import ChatRepository


class ChatService:

    def __init__(
            self,
            repository: ChatRepository
    ):
        self.__repository = repository

    async def get_chat_by_id(self, chat_id: UUID):
        chat = await self.__repository.get_chat_by_id(chat_id)
        return chat

    async def user_in_chat(self, chat: Chat, user_id: UUID):
        user_in_chat = await self.__repository.user_in_chat(chat, user_id)
        return user_in_chat

    async def get_chats_by_user_id(self, user_id: UUID):
        chats = await self.__repository.get_chats_by_user_id(user_id)
        return chats

    async def get_direct_chat_by_user_ids(self, first_user_id: UUID, second_user_id: UUID):
        chat = await self.__repository.get_direct_chat_by_user_ids(first_user_id, second_user_id)
        return chat

    async def create_direct_chat(self, chat_create: ChatCreate, create_date: str):
        await self.__repository.create_direct_chat(chat_create, create_date)

    async def update_chat_activity(self, chat_id: UUID, activity_date: str):
        await self.__repository.update_chat_activity(chat_id, activity_date)

    async def delete_chat_by_id(self, chat_id: UUID):
        await self.__repository.delete_chat_by_id(chat_id)
