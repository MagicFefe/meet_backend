from uuid import UUID
from fastapi_pagination import Params
from models.message.message_send import MessageSend
from repositories.message.message_repository import MessageRepository


class MessageService:

    def __init__(
            self,
            repository: MessageRepository
    ):
        self.__repository = repository

    async def save_message(self, message: MessageSend, chat_id: UUID, user_id: UUID, current_date: str):
        await self.__repository.save_message(message, chat_id, user_id, current_date)

    async def get_chat_messages(self, chat_id: UUID, user_id: UUID, pagination_prams: Params):
        page = await self.__repository.get_chat_messages(chat_id, user_id, pagination_prams)
        return page

    async def get_message(self, chat_id: UUID, user_id: UUID, send_date: str):
        message = await self.__repository.get_message(chat_id, user_id, send_date)
        return message

    async def mark_as_read(self, chat_id: UUID, user_id: UUID, last_read_message_date: str | None):
        await self.__repository.mark_as_read(chat_id, user_id, last_read_message_date)
