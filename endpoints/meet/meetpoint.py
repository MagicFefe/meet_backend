from json import loads
from aioredis import Redis
from fastapi import APIRouter, WebSocket, Depends
from dependencies import get_meets_repository, get_redis_db
from endpoints.meet.event_holder import EventHolder, MeetAdded, Event
from models.meet.meet import Meet
from repositories.meet_repository import MeetRepository
from utils.data.data_observer import DataObserver

router = APIRouter(prefix="/api/meet", tags=["meet"])
event_holder = EventHolder()


@router.websocket(path="/ws")
async def receive_meets(
        websocket: WebSocket,
        meets_db: Redis = Depends(get_redis_db),
        meets_repository: MeetRepository = Depends(get_meets_repository)
):
    async def handle_event(event: Event):
        data = await meets_repository.get_meets(meets_db)
        await websocket.send_json(
            {
                "meets": data
            }
        )

    observer = DataObserver(on_next=handle_event)
    await websocket.accept()
    while True:
        await event_holder.event.subscribe(
            observer
        )
        try:
            client_message = await websocket.receive_json()
            if loads(client_message)["action"] == "close":
                await websocket.close()
        except:
            return


@router.post(
    path=""
)
async def create_meet(
        meet: Meet,
        meets_db: Redis = Depends(get_redis_db),
        meets_repository: MeetRepository = Depends(get_meets_repository)
):
    await meets_repository.create_meet(meets_db, meet)
    await event_holder.update_event(MeetAdded())
    return
