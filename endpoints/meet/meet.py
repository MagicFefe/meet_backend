from json import loads
from aioredis import Redis
from fastapi import APIRouter, WebSocket, Depends
from dependencies import get_meet_repository, get_redis_db, get_user_repository, get_session
from endpoints.meet.event_holder import EventHolder, MeetAdded, Event, MeetDeleted
from models.meet.meet import Meet
from repositories.meet_repository import MeetRepository
from utils.data.data_observer import DataObserver
from starlette.websockets import WebSocketState
from models.meet.meet_response_details import MeetResponseDetails
from repositories.user_repository import UserRepository
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from files.file_manager import FileManager
from config import USER_IMAGE_FILE_STORAGE_PATH

router = APIRouter(
    prefix="/api/meet",
    tags=["meet"]
)
event_holder = EventHolder()


@router.websocket(path="/ws")
async def receive_meets(
        websocket: WebSocket,
        meet_db: Redis = Depends(get_redis_db),
        meet_repository: MeetRepository = Depends(get_meet_repository)
):
    await websocket.accept()

    # TODO: create cheking auth token in header
    async def handle_event(event: Event):
        if websocket.application_state == WebSocketState.CONNECTED:
            meets = await meet_repository.get_meets(meet_db)
            result = []
            for meet in meets:
                result.append(meet.dict())
            await websocket.send_json(result)

    observer = DataObserver(on_next=handle_event)

    while True:
        await event_holder.event.subscribe(
            observer
        )
        try:
            client_message = await websocket.receive_json()
            if loads(client_message)["action"] == "close":
                event_holder.event.unsubscribe(observer)
                await websocket.close()
        except:
            event_holder.event.unsubscribe(observer)
            return


@router.post(
    path=""
)
async def create_meet(
        meet: Meet,
        meet_db: Redis = Depends(get_redis_db),
        meet_repository: MeetRepository = Depends(get_meet_repository)
):
    await meet_repository.create_meet(meet_db, meet)
    await event_holder.update_event(MeetAdded())
    return


@router.get(
    path="/{meet_id}",
    response_model=MeetResponseDetails
)
async def get_meet_by_id(
        meet_id: str,
        meet_db: Redis = Depends(get_redis_db),
        meet_repository: MeetRepository = Depends(get_meet_repository),
        user_db_session: AsyncSession = Depends(get_session),
        user_repository: UserRepository = Depends(get_user_repository)
):
    image_file_manger: FileManager = FileManager(USER_IMAGE_FILE_STORAGE_PATH)
    try:
        meet = await meet_repository.get_meet_by_id(meet_db, meet_id)
    except Exception:
        raise HTTPException(status_code=422, detail="invalid id")
    user = await user_repository.get_user_by_id(user_db_session, UUID(meet.author_id))
    if user is None:
        raise HTTPException(status_code=422, detail="user does not exist")
    meet_details = MeetResponseDetails(
        id=meet.id,
        author_id=meet.author_id,
        author_name=user.name,
        author_surname=user.surname,
        author_image=image_file_manger.read_file(user.image_path),
        meet_name=meet.meet_name,
        meet_description=meet.meet_description,
        latitude=meet.latitude,
        longitude=meet.longitude,
        created_at=meet.created_at
    )
    return meet_details


@router.delete(
    path="/{meet_id}"
)
async def delete_meet(
        meet_id: str,
        meet_db: Redis = Depends(get_redis_db),
        meet_repository: MeetRepository = Depends(get_meet_repository)
):
    await meet_repository.delete_meet(meet_db, meet_id)
    await event_holder.update_event(MeetDeleted())
