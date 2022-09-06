from uuid import UUID
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from fastapi_pagination import Params
from di.application_container import ApplicationContainer
from request_checkers.chat_membership_check import check_chat_membership
from services.message.message_service import MessageService

router = APIRouter(
    prefix="/api/message",
    tags=["message"],
    dependencies=[
        Depends(check_chat_membership)
    ]
)


@router.get(
    path="/{chat_id}"
)
@inject
async def get_chat_messages(
        chat_id: str,
        user_id: str = Depends(check_chat_membership),
        pagination_params: Params = Depends(),
        message_service: MessageService = Depends(Provide[ApplicationContainer.service_container.message_service])
):
    messages = await message_service.get_chat_messages(UUID(chat_id), UUID(user_id), pagination_params)
    return messages


@router.post(
    path="/{chat_id}"
)
@inject
async def mark_message_as_read(
        chat_id: str,
        read_date: str,
        user_id: str = Depends(check_chat_membership),
        message_service: MessageService = Depends(Provide[ApplicationContainer.service_container.message_service])
):
    await message_service.mark_as_read(UUID(chat_id), UUID(user_id), read_date)
