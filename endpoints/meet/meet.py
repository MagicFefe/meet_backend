from json import loads
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, WebSocket, Depends
from starlette import status
from di.application_container import ApplicationContainer
from endpoints.meet.event_holder import EventHolder, MeetAdded, Event, MeetDeleted, MeetUpdated
from exceptions import MeetPointAlreadyExistsError
from files.file_manager import FileManager
from models.meet.mappers.mappers import from_meet_response_to_meet_response_details
from models.meet.meet import Meet
from models.meet.meet_delete import MeetDelete
from models.meet.meet_update import MeetUpdate
from services.meet.meet_service import MeetService
from services.user.user_service import UserService
from utils.observable_data.data_observer import DataObserver
from starlette.websockets import WebSocketState
from models.meet.meet_response_details import MeetResponseDetails
from uuid import UUID
from fastapi import HTTPException
from request_checkers.ws_check_request import check_ws_header

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
        service: MeetService = Depends(Provide[ApplicationContainer.service_container.meet_service]),
        event_holder: EventHolder = Depends(Provide[ApplicationContainer.meet_container.event_holder])
):
    await websocket.accept()
    await check_ws_header(websocket)

    async def handle_event(event: Event):
        if websocket.application_state == WebSocketState.CONNECTED:
            meets = await service.get_meets()
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
        service: MeetService = Depends(Provide[ApplicationContainer.service_container.meet_service]),
        event_holder: EventHolder = Depends(Provide[ApplicationContainer.meet_container.event_holder])
):
    try:
        await service.create_meet(meet)
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
        meet_service: MeetService = Depends(Provide[ApplicationContainer.service_container.meet_service]),
        user_service: UserService = Depends(Provide[ApplicationContainer.service_container.user_service]),
        image_file_manager: FileManager = Depends(
            Provide[ApplicationContainer.file_storage_container.user_image_file_manager]
        )
):
    try:
        meet = await meet_service.get_meet_by_id(meet_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="invalid id")
    user = await user_service.get_user_by_id(UUID(meet.author_id))
    if user is None:
        await meet_service.delete_invalid_meet(meet_id)
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="user does not exist")
    meet_details = from_meet_response_to_meet_response_details(meet, user, image_file_manager)
    return meet_details


@router.put(
    path=""
)
@inject
async def update_meet(
        meet_update: MeetUpdate,
        service: MeetService = Depends(Provide[ApplicationContainer.service_container.meet_service]),
        event_holder: EventHolder = Depends(Provide[ApplicationContainer.meet_container.event_holder])
):
    await service.update_meet(meet_update)
    await event_holder.update_event(MeetUpdated())


@router.delete(
    path=""
)
@inject
async def delete_meet(
        meet_delete: MeetDelete,
        service: MeetService = Depends(Provide[ApplicationContainer.service_container.meet_service]),
        event_holder: EventHolder = Depends(Provide[ApplicationContainer.meet_container.event_holder])
):
    await service.delete_meet(meet_delete)
    await event_holder.update_event(MeetDeleted())
