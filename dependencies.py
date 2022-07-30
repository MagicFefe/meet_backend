from endpoints.meet.event_holder import EventHolder
from repositories.user_repository import UserRepository
from repositories.meet_repository import MeetRepository
from aioredis import Redis, from_url
from config import MEET_DB_URL, ENCODING


async def get_session() -> None:
    pass


async def get_meet_db() -> Redis:
    return from_url(MEET_DB_URL, encoding=ENCODING)


async def get_event_holder() -> EventHolder:
    return EventHolder()


async def get_user_repository() -> UserRepository:
    return UserRepository()


async def get_meet_repository() -> MeetRepository:
    return MeetRepository()
