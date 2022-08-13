from models.meet.meet import Meet
from models.meet.meet_delete import MeetDelete
from models.meet.meet_update import MeetUpdate
from repositories.meet.meet_repository import MeetRepository


class MeetService:
    def __init__(
            self,
            repository: MeetRepository
    ):
        self.__repository = repository

    async def create_meet(self, meet: Meet):
        await self.__repository.create_meet(meet)

    async def get_meets(self):
        meets = await self.__repository.get_meets()
        return meets

    async def get_meet_by_id(self, meet_id: str):
        meet = await self.__repository.get_meet_by_id(meet_id)
        return meet

    async def update_meet(self, meet: MeetUpdate):
        await self.__repository.update_meet(meet)

    async def delete_meet(self, meet: MeetDelete):
        await self.__repository.delete_meet(meet)

    async def delete_invalid_meet(self, meet_id: str):
        await self.__repository.delete_invalid_meet(meet_id)
