from repositories.user_repository import UserRepository
from repositories.meet_repository import MeetRepository
from aioredis import Redis, from_url
from config import REDIS_DB_URL, ENCODING


async def get_session() -> None:
    pass


async def get_redis_db() -> Redis:
    return from_url(REDIS_DB_URL, encoding=ENCODING)


async def get_user_repository() -> UserRepository:
    return UserRepository()


async def get_meets_repository() -> MeetRepository:
    return MeetRepository()
