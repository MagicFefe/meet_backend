from datetime import datetime
from json import dumps
from uuid import UUID
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from starlette import status
from starlette.exceptions import HTTPException
from starlette.websockets import WebSocket, WebSocketDisconnect
from config import DATETIME_PATTERN
from db.enitites.chat.chat import Chat
from db.enitites.chat.mappers.mappers import from_chat_to_chat_response
from db.enitites.message.mappers.mappers import from_message_to_message_response
from db.enitites.user.user import User
from di.application_container import ApplicationContainer
from endpoints.chat.chat_events import ChatListEvent, NewChatCreated, NewMessageInChatSent, ChatDeleted
from models.chat.chat_create import ChatCreate
from models.chat.chat_response import ChatResponse
from request_checkers.chat_membership_check import ws_check_chat_membership, check_chat_membership
from request_checkers.ws_check_request import check_ws_header
from services.chat.chat_service import ChatService
from models.message.message_send import MessageSend
from services.message.message_service import MessageService
from utils.event_holder.event_holder import EventHolder
from utils.observable_data.data_observer import DataObserver
from utils.ws_connectivity_manager.ws_connectivity_manager import WSConnectivityManager

router = APIRouter(
    prefix="/api/chat",
    tags=["chat"]
)


@router.websocket(
    path="/list"
)
@inject
async def list_chats(
        websocket: WebSocket,
        chat_service: ChatService = Depends(Provide[ApplicationContainer.service_container.chat_service]),
        chat_list_connections_manager: WSConnectivityManager = Depends(
            Provide[ApplicationContainer.chat_container.chat_list_connections_manager]
        ),
        chat_list_event_holder: EventHolder[ChatListEvent] = Depends(
            Provide[ApplicationContainer.chat_container.chat_list_event_holder]
        )
):
    await chat_list_connections_manager.connect(websocket)
    user: User = await check_ws_header(websocket, chat_list_connections_manager)

    async def on_event(event: ChatListEvent):
        chats = await chat_service.get_chats_by_user_id(user.id)
        converted = [from_chat_to_chat_response(chat) for chat in chats]
        await chat_list_connections_manager.send_json_to_websocket(
            [chat.dict() for chat in converted], websocket
        )

    observer = DataObserver(on_next=on_event)

    try:
        while True:
            await chat_list_event_holder.event.subscribe(observer)
            await websocket.receive_json()
    except WebSocketDisconnect:
        await chat_list_connections_manager.remove_connection(websocket)


@router.websocket(
    path="/{chat_id}/start",
)
@inject
async def start_chat(
        websocket: WebSocket,
        chat_id: str,
        message_service: MessageService = Depends(Provide[ApplicationContainer.service_container.message_service]),
        chat_service: ChatService = Depends(Provide[ApplicationContainer.service_container.chat_service]),
        chat_connections_manager: WSConnectivityManager = Depends(
            Provide[ApplicationContainer.chat_container.chat_connections_manager]
        ),
        chat_list_event_holder: EventHolder[ChatListEvent] = Depends(
            Provide[ApplicationContainer.chat_container.chat_list_event_holder]
        )
):
    await chat_connections_manager.connect(websocket)
    user_id = await ws_check_chat_membership(websocket, chat_connections_manager)

    try:
        while True:
            message_json = await websocket.receive_json()
            message = MessageSend.parse_raw(dumps(message_json))
            # drop last 3 symbols because time resolution of client is milliseconds
            send_date = datetime.utcnow().strftime(DATETIME_PATTERN)[0:-3]
            await message_service.save_message(message, UUID(chat_id), UUID(user_id), send_date)
            message_db = await message_service.get_message(UUID(chat_id), UUID(user_id), send_date)
            message_response = from_message_to_message_response(message_db)
            if not (message_db is None):
                await chat_connections_manager.send_json_broadcast(message_response.dict())
                await chat_service.update_chat_activity(UUID(chat_id), send_date)
                await chat_list_event_holder.update_event(NewMessageInChatSent())
    except WebSocketDisconnect:
        await chat_connections_manager.remove_connection(websocket)


@router.post(
    path="",
    response_model=ChatResponse
)
@inject
async def create_chat(
        chat_create: ChatCreate,
        service: ChatService = Depends(Provide[ApplicationContainer.service_container.chat_service]),
        chat_list_event_holder: EventHolder[ChatListEvent] = Depends(
            Provide[ApplicationContainer.chat_container.chat_list_event_holder]
        )
):
    user_ids = list(map(lambda item: UUID(item), chat_create.users))
    if len(user_ids) == 2:
        create_date = datetime.utcnow().strftime(DATETIME_PATTERN)
        existing_direct_chat = await service.create_direct_chat(chat_create, create_date)
        chat_for_mapper: Chat
        if existing_direct_chat is Chat:
            chat_for_mapper = existing_direct_chat
        else:
            created_chat = await service.get_direct_chat_by_user_ids(user_ids[0], user_ids[1])
            chat_for_mapper = created_chat
            await chat_list_event_holder.update_event(NewChatCreated())
        return from_chat_to_chat_response(chat_for_mapper)
    else:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="chat can be created between at least two users"
        )


@router.get(
    path="/{user_id}/all",
    response_model=list[ChatResponse]
)
@inject
async def get_user_chats(
        user_id: str,
        service: ChatService = Depends(Provide[ApplicationContainer.service_container.chat_service])
):
    chats = await service.get_chats_by_user_id(UUID(user_id))
    if not (chats is None):
        return [from_chat_to_chat_response(chat) for chat in chats]
    return []


@router.delete(
    path="/{chat_id}",
    dependencies=[
        Depends(
            check_chat_membership
        )
    ]
)
@inject
async def delete_chat_by_id(
        chat_id: str,
        service: ChatService = Depends(Provide[ApplicationContainer.service_container.chat_service]),
        chat_list_event_holder: EventHolder[ChatListEvent] = Depends(
            Provide[ApplicationContainer.chat_container.chat_list_event_holder]
        )
):
    await service.delete_chat_by_id(UUID(chat_id))
    await chat_list_event_holder.update_event(ChatDeleted())
