from json import loads
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, WebSocket, Depends
from starlette import status
from di.application_container import ApplicationContainer
from endpoints.meet.event_holder import EventHolder, MeetAdded, Event, MeetDeleted, MeetUpdated
from exceptions import MeetPointAlreadyExistsError
from models.meet.meet import Meet
from models.meet.meet_delete import MeetDelete
from models.meet.meet_update import MeetUpdate
from repositories.meet_repository import MeetRepository
from utils.observable_data.data_observer import DataObserver
from starlette.websockets import WebSocketState
from models.meet.meet_response_details import MeetResponseDetails
from repositories.user_repository import UserRepository
from uuid import UUID
from fastapi import HTTPException
from files.file_manager import FileManager
from config import USER_IMAGE_FILE_STORAGE_PATH
from utils.saveable_list.saveable_list import SaveableList

router = APIRouter(
    prefix="/api/meet",
    tags=["meet"]
)


@router.websocket(
    path="/ws"
)
@inject
async def receive_meets(
        websocket: WebSocket,
        meet_repository: MeetRepository = Depends(Provide[ApplicationContainer.repository_container.meet_repository]),
        event_holder: EventHolder = Depends(Provide[ApplicationContainer.meet_container.event_holder])
):
    await websocket.accept()

    # TODO: create checking auth token in header
    async def handle_event(event: Event):
        if websocket.application_state == WebSocketState.CONNECTED:
            meets = await meet_repository.get_meets()
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
@inject
async def create_meet(
        meet: Meet,
        meet_repository: MeetRepository = Depends(Provide[ApplicationContainer.repository_container.meet_repository]),
        event_holder: EventHolder = Depends(Provide[ApplicationContainer.meet_container.event_holder]),
        meet_authors_id_storage: SaveableList = Depends(Provide[ApplicationContainer.meet_authors_id_storage])
):
    try:
        await meet_repository.create_meet(meet_authors_id_storage.items, meet)
        await event_holder.update_event(MeetAdded())
    except MeetPointAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="meet point with this author's id already exists"
        )
    return


@router.get(
    path="/{meet_id}",
    response_model=MeetResponseDetails
)
@inject
async def get_meet_by_id(
        meet_id: str,
        meet_repository: MeetRepository = Depends(Provide[ApplicationContainer.repository_container.meet_repository]),
        user_repository: UserRepository = Depends(Provide[ApplicationContainer.repository_container.user_repository])
):
    image_file_manger: FileManager = FileManager(USER_IMAGE_FILE_STORAGE_PATH)
    try:
        meet = await meet_repository.get_meet_by_id(meet_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="invalid id")
    user = await user_repository.get_user_by_id(UUID(meet.author_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="user does not exist")
    meet_details = MeetResponseDetails(
        id=meet.id,
        author_id=meet.author_id,
        author_name=user.name,
        author_surname=user.surname,
        author_image=image_file_manger.read_file(user.image_filename),
        meet_name=meet.meet_name,
        meet_description=meet.meet_description,
        latitude=meet.latitude,
        longitude=meet.longitude,
        created_at=meet.created_at
    )
    return meet_details


@router.put(
    path=""
)
@inject
async def update_meet(
        meet_update: MeetUpdate,
        meet_repository: MeetRepository = Depends(Provide[ApplicationContainer.repository_container.meet_repository]),
        event_holder: EventHolder = Depends(Provide[ApplicationContainer.meet_container.event_holder])
):
    await meet_repository.update_meet(meet_update)
    await event_holder.update_event(MeetUpdated())


@router.delete(
    path=""
)
@inject
async def delete_meet(
        meet_delete: MeetDelete,
        meet_repository: MeetRepository = Depends(Provide[ApplicationContainer.repository_container.meet_repository]),
        event_holder: EventHolder = Depends(Provide[ApplicationContainer.meet_container.event_holder]),
        meet_authors_id_storage: SaveableList = Depends(Provide[ApplicationContainer.meet_authors_id_storage])
):
    await meet_repository.delete_meet(meet_authors_id_storage.items, meet_delete)
    await event_holder.update_event(MeetDeleted())
