from datetime import datetime
from functools import reduce
from typing import AsyncIterator, Callable
from sqlalchemy import delete, intersect, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from config import DATETIME_PATTERN
from db.enitites.chat.chat import Chat
from db.enitites.user.user import User
from db.enitites.user_chat_assoc.user_chat_assoc import UserChatAssociation
from models.chat.chat_create import ChatCreate
from repositories.user.user_repository import UserRepository
from uuid import UUID
from re import split


class ChatRepository:
    def __init__(
            self,
            db_session: Callable[[], AsyncIterator[AsyncSession]],
            user_repository: UserRepository
    ):
        self.__db_session = db_session
        self.__user_repository = user_repository

    async def get_chat_by_id(self, chat_id: UUID) -> Chat | None:
        async with self.__db_session() as session:
            chat = await session.execute(select(Chat).where(Chat.id == chat_id))
            return chat.scalar_one_or_none()

    async def user_in_chat(self, chat: Chat, user_id: UUID) -> bool:
        async with self.__db_session():
            if chat is None:
                return False
            return any([user.id == user_id for user in chat.users])

    async def get_direct_chat_by_user_ids(self, first_user_id: UUID, second_user_id: UUID) -> Chat | None:
        async with self.__db_session() as session:
            rows_with_searched_users = await session.execute(
                intersect(
                    select(UserChatAssociation.chat_id).where(
                        UserChatAssociation.user_id == first_user_id
                    ),
                    select(UserChatAssociation.chat_id).where(
                        UserChatAssociation.user_id == second_user_id
                    )
                )
            )
            chat_ids_with_searched_users = rows_with_searched_users.scalars()
            direct_chat = await session.execute(
                select(Chat).where(
                    (Chat.id.in_(chat_ids_with_searched_users)) & (Chat.chat_name == None)
                )
            )
            return direct_chat.scalar_one_or_none()

    async def get_chats_by_user_id(self, user_id: UUID) -> list[Chat] | None:
        async with self.__db_session() as session:
            user = await session.execute(
                select(User).where(User.id == user_id)
            )
            user = user.scalar_one_or_none()
            if user is None:
                return None
            else:
                chats = await session.execute(
                    select(Chat).where(Chat.id.in_([chat.id for chat in user.chats]))
                )
                chats = chats.scalars()
                return sorted(
                    chats,
                    key=lambda chat: int(
                        reduce(
                            lambda acc, item: acc + item,
                            split(r"[-\s:.]", datetime.strftime(chat.last_activity_date, DATETIME_PATTERN))
                        )
                    ),
                    reverse=True
                )

    async def create_direct_chat(self, chat_create: ChatCreate, create_date: str) -> Chat:
        async with self.__db_session() as session:
            user_ids = list(map(lambda item: UUID(item), chat_create.users))
            chat_db = await self.get_direct_chat_by_user_ids(user_ids[0], user_ids[1])
            chat_not_exists = chat_db is None
            if chat_not_exists:
                users = await self.__user_repository.get_users_by_ids(user_ids)
                new_chat = Chat()
                new_chat.users.extend(users)
                new_chat.last_activity_date = datetime.strptime(create_date, DATETIME_PATTERN)
                session.add(new_chat)
                await session.commit()
            else:
                return chat_db

    async def update_chat_activity(self, chat_id: UUID, activity_date: str):
        async with self.__db_session() as session:
            await session.execute(
                update(Chat).where(Chat.id == chat_id).values(
                    last_activity_date=datetime.strptime(activity_date, DATETIME_PATTERN)
                )
            )
            await session.commit()

    async def delete_chat_by_id(self, chat_id: UUID):
        async with self.__db_session() as session:
            chat = await self.get_chat_by_id(chat_id)
            if not (chat is None):
                await session.execute(delete(UserChatAssociation).where(UserChatAssociation.chat_id == chat_id))
                await session.execute(delete(Chat).where(Chat.id == chat_id))
                await session.commit()
