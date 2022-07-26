from typing import Any

from aioredis import Redis
from models.meet.meet import Meet
from uuid import uuid4
from models.meet.meet_db import MeetDB
from models.meet.meet_response import MeetResponse
from datetime import datetime


def decode_meet_from_bytes(meet_bytes: Any) -> dict[str, str]:
    meet: dict[str, str] = {}
    for id, value in meet_bytes.items():
        meet[id.decode("utf-8")] = value.decode("utf-8")
    return meet


class MeetRepository:
    async def create_meet(self, meet_db: Redis, meet: Meet):
        async with meet_db.client() as connection:
            meet_db = from_meet_to_meet_db(meet)
            await connection.hset(meet_db.id, mapping=meet_db.dict())

    async def get_meets(self, meets_db: Redis):
        async with meets_db.client() as connection:
            keys = await connection.keys()
            meets = []
            for key in keys:
                meet_bytes = await connection.hgetall(key)
                meet = decode_meet_from_bytes(meet_bytes)
                meets.append(from_dict_to_meet_response(meet))
        return meets

    async def get_meet_by_id(self, meet_db: Redis, meet_id: str):
        async with meet_db.client() as connection:
            meet_bytes = await connection.hgetall(meet_id)
        meet_dict = decode_meet_from_bytes(meet_bytes)
        meet = from_dict_to_meet_response(meet_dict)
        return meet

    async def delete_meet(self, meet_db: Redis, meet_id: str):
        async with meet_db.client() as connection:
            await connection.delete(meet_id)


def from_meet_to_meet_db(meet: Meet) -> MeetDB:
    meet_id = str(uuid4())
    date = str(datetime.now())
    meet_db = MeetDB(
        id=meet_id,
        meet_description=meet.meet_description,
        meet_name=meet.meet_name,
        author_name=meet.author_name,
        author_surname=meet.author_surname,
        author_id=meet.author_id,
        latitude=meet.latitude,
        longitude=meet.longitude,
        created_at=date
    )
    return meet_db


def from_meet_db_to_meet_response(meet_db: MeetDB) -> MeetResponse:
    return MeetResponse(
        id=meet_db.id,
        author_id=meet_db.author_id,
        meet_name=meet_db.meet_name,
        meet_description=meet_db.meet_description,
        latitude=meet_db.latitude,
        longitude=meet_db.longitude,
        created_at=meet_db.created_at
    )


def from_dict_to_meet_response(meet_dict: dict[str, str]) -> MeetResponse:
    return MeetResponse(
        id=meet_dict["id"],
        author_id=meet_dict["author_id"],
        meet_name=meet_dict["meet_name"],
        meet_description=meet_dict["meet_description"],
        latitude=meet_dict["latitude"],
        longitude=meet_dict["longitude"],
        created_at=meet_dict["created_at"]
    )
