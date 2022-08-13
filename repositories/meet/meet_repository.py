from typing import Any
from aioredis import Redis
from exceptions import MeetPointAlreadyExistsError
from models.meet.mappers.mappers import from_meet_to_meet_db
from models.meet.meet import Meet
from models.meet.meet_delete import MeetDelete
from models.meet.meet_response import MeetResponse
from models.meet.meet_update import MeetUpdate
from utils.saveable_list.saveable_list import SaveableList


class MeetRepository:
    def __init__(
            self,
            meet_db: Redis,
            meet_authors_id_storage: SaveableList
    ):
        self.__meet_db = meet_db
        self.__meet_authors_id_storage = meet_authors_id_storage

    async def create_meet(self, meet: Meet):
        meet_author_list: list[str] = self.__meet_authors_id_storage.items
        if meet.author_id in meet_author_list:
            raise MeetPointAlreadyExistsError()
        else:
            meet_author_list.append(meet.author_id)
        async with self.__meet_db.client() as connection:
            meet_db_model = from_meet_to_meet_db(meet)
            await connection.hset(meet_db_model.id, mapping=meet_db_model.dict())

    async def get_meets(self):
        async with self.__meet_db.client() as connection:
            keys = await connection.keys()
            meets = []
            for key in keys:
                meet_bytes = await connection.hgetall(key)
                meet = decode_meet_from_bytes(meet_bytes)
                meets.append(from_dict_to_meet_response(meet))
        return meets

    async def get_meet_by_id(self, meet_id: str):
        async with self.__meet_db.client() as connection:
            meet_bytes = await connection.hgetall(meet_id)
        meet_dict = decode_meet_from_bytes(meet_bytes)
        meet = from_dict_to_meet_response(meet_dict)
        return meet

    async def update_meet(self, meet: MeetUpdate):
        async with self.__meet_db.client() as connection:
            await connection.hset(meet.id, mapping=meet.dict())

    async def delete_meet(self, meet: MeetDelete):
        meet_author_list: list[str] = self.__meet_authors_id_storage.items
        async with self.__meet_db.client() as connection:
            await connection.delete(meet.id)
        if meet.author_id in meet_author_list:
            meet_author_list.remove(meet.author_id)

    async def delete_invalid_meet(self, meet_id: str):
        async with self.__meet_db.client() as connection:
            await connection.delete(meet_id)


def decode_meet_from_bytes(meet_bytes: Any) -> dict[str, str]:
    meet: dict[str, str] = {}
    for id, value in meet_bytes.items():
        meet[id.decode("utf-8")] = value.decode("utf-8")
    return meet


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
