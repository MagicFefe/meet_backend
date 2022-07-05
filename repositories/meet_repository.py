from aioredis import Redis
from models.meet.meet import Meet
from uuid import uuid4
from models.meet.meet_db import MeetDB
from datetime import datetime


class MeetRepository:
    async def create_meet(self, meets_db: Redis, meet: Meet):
        async with meets_db.client() as connection:
            meet_db = from_meet_to_meet_db(meet)
            await connection.hset(meet_db.id, mapping=meet_db.dict())

    async def get_meets(self, meets_db: Redis):
        async with meets_db.client() as connection:
            keys = await connection.keys()
            meets = []
            for key in keys:
                meet_bytes = await connection.hgetall(key)
                meet: dict[str, str] = {}
                for id, value in meet_bytes.items():
                    meet[id.decode("utf-8")] = value.decode("utf-8")
                meets.append(meet)
        return meets


def from_meet_to_meet_db(meet: Meet) -> MeetDB:
    meet_id = str(uuid4())
    date = str(datetime.now())
    meet_db = MeetDB(
        id=meet_id,
        meet_description=meet.meet_description,
        meet_name=meet.meet_name,
        author_name=meet.author.author_name,
        author_surname=meet.author.author_surname,
        author_id=meet.author.author_id,
        created_at=date
    )
    return meet_db
