from logging import getLogger
from typing import Mapping
from uuid import UUID
from dependency_injector.wiring import inject, Provide
from fastapi import Depends
from starlette import status
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.websockets import WebSocket
from db.enitites.user.user import User
from di.application_container import ApplicationContainer
from exceptions import ChatDoesNotExistError, UserNotInChatError, UserDoesNotExistError
from services.chat.chat_service import ChatService
from services.user.user_service import UserService
from utils.authorization_utils import authorize_user
from utils.ws_connectivity_manager.ws_connectivity_manager import WSConnectivityManager


async def _check_chat_membership(
        headers: Mapping[str, str],
        path_params: Mapping[str, str],
        user_service: UserService,
        chat_service: ChatService
):
    user: User = await authorize_user(headers, user_service)
    user_id = user.id
    chat_id = path_params.get("chat_id")
    getLogger("foo-logger").debug(chat_id)
    if chat_id is None:
        raise KeyError()

    chat = await chat_service.get_chat_by_id(UUID(chat_id))
    if chat is None:
        raise ChatDoesNotExistError()

    user_in_chat = await chat_service.user_in_chat(chat, user_id)
    if not user_in_chat:
        raise UserNotInChatError()

    return str(user_id)


@inject
async def check_chat_membership(
        request: Request,
        user_service: UserService = Depends(Provide[ApplicationContainer.service_container.user_service]),
        chat_service: ChatService = Depends(Provide[ApplicationContainer.service_container.chat_service])
):
    try:
        user_id = await _check_chat_membership(
            request.headers,
            request.path_params,
            user_service,
            chat_service
        )
        return user_id
    except KeyError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"unauthorized request")
    except UserDoesNotExistError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user does not exist")
    except ChatDoesNotExistError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="chat does not exist")
    except UserNotInChatError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="user not in this chat")
    except Exception:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="invalid token")


@inject
async def ws_check_chat_membership(
        ws: WebSocket,
        chat_connections_manager: WSConnectivityManager | None = None,
        user_service: UserService = Provide[ApplicationContainer.service_container.user_service],
        chat_service: ChatService = Provide[ApplicationContainer.service_container.chat_service]
):
    async def on_error(reason: str, code: int = status.WS_1008_POLICY_VIOLATION):
        if chat_connections_manager is None:
            await ws.close(code, reason)
        else:
            await chat_connections_manager.disconnect(ws, code, reason)

    try:
        user_id = await _check_chat_membership(
            ws.headers, ws.path_params, user_service, chat_service
        )
        return user_id
    except KeyError:
        await on_error("unauthorized attempt connection")
    except UserDoesNotExistError:
        await on_error("user does not exist")
    except ChatDoesNotExistError:
        await on_error("chat does not exist")
    except UserNotInChatError:
        await on_error("user not in this chat")
