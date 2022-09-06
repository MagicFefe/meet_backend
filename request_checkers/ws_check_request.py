from dependency_injector.wiring import inject, Provide
from starlette import status
from starlette.websockets import WebSocket
from di.application_container import ApplicationContainer
from exceptions import UserDoesNotExistError
from services.user.user_service import UserService
from utils.authorization_utils import authorize_user
from utils.ws_connectivity_manager.ws_connectivity_manager import WSConnectivityManager


@inject
async def check_ws_header(
        ws: WebSocket,
        chat_connections_manager: WSConnectivityManager | None = None,
        service: UserService = Provide[ApplicationContainer.service_container.user_service]
):
    async def on_error(reason: str, code: int = status.WS_1008_POLICY_VIOLATION):
        if chat_connections_manager is None:
            await ws.close(code, reason)
        else:
            await chat_connections_manager.disconnect(ws, code, reason)

    try:
        user = await authorize_user(ws.headers, service)
        return user
    except KeyError:
        await on_error("unauthorized attempt connection")
    except UserDoesNotExistError:
        await on_error("user does not exist")
    except:
        await ws.close(code=status.WS_1008_POLICY_VIOLATION, reason="token is invalid")
