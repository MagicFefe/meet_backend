from datetime import datetime
from typing import Callable, AsyncIterator, Any
from uuid import UUID
from fastapi_pagination import Params
from fastapi_pagination.ext.async_sqlalchemy import paginate
from sqlalchemy import select, desc, update
from sqlalchemy.ext.asyncio import AsyncSession
from config import DATETIME_PATTERN
from db.enitites.user_chat_assoc.user_chat_assoc import UserChatAssociation
from models.message.mappers.mappers import from_message_send_to_message
from models.message.message_send import MessageSend
from db.enitites.message.message import Message as MessageDB


class MessageRepository:

    def __init__(
            self,
            db_session: Callable[[], AsyncIterator[AsyncSession]]
    ):
        self.__db_session = db_session

    async def save_message(self, message: MessageSend, chat_id: UUID, user_id: UUID, current_date: str):
        current_date_datetime = datetime.strptime(current_date, DATETIME_PATTERN)
        async with self.__db_session() as session:
            session.add(
                from_message_send_to_message(message, chat_id, user_id, current_date_datetime)
            )
            await session.commit()

    async def get_chat_messages(self, chat_id: UUID, user_id: UUID, pagination_prams: Params):
        async with self.__db_session() as session:
            association = await session.execute(
                select(UserChatAssociation).where(
                    (UserChatAssociation.chat_id == chat_id) & (UserChatAssociation.user_id == user_id)
                )
            )
            association = association.scalar_one_or_none()
            if association is None:
                return None
            condition = (MessageDB.chat_id == chat_id)
            if not(association.last_read_message_date is None):
                condition = (condition & (MessageDB.send_date > association.last_read_message_date))
            page = await paginate(
                session,
                select(MessageDB).where(condition).order_by(desc(MessageDB.send_date)),
                pagination_prams
            )
            return page

    async def get_message(self, chat_id: UUID, user_id: UUID, send_date: str) -> MessageDB | None:
        send_date = datetime.strptime(send_date, DATETIME_PATTERN)
        async with self.__db_session() as session:
            message = await session.execute(
                select(MessageDB).where(
                    (MessageDB.chat_id == chat_id) & (MessageDB.user_id == user_id) & (MessageDB.send_date == send_date)
                )
            )
            return message.scalar_one_or_none()

    async def mark_as_read(self, chat_id: UUID, user_id: UUID, last_read_message_date: str | None):
        async with self.__db_session() as session:
            read_date: datetime | None
            if last_read_message_date is None:
                read_date = None
            else:
                read_date = datetime.strptime(last_read_message_date, DATETIME_PATTERN)
            await session.execute(
                update(UserChatAssociation).where(
                    (UserChatAssociation.chat_id == chat_id) & (UserChatAssociation.user_id == user_id)
                ).values(
                    last_read_message_date=read_date
                )
            )
            await session.commit()
