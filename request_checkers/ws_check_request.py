from dependency_injector.wiring import inject, Provide
from starlette import status
from starlette.websockets import WebSocket
from di.application_container import ApplicationContainer
from services.user.user_service import UserService
from utils.authorization_utils import authorize_user


@inject
async def check_ws_header(
        ws: WebSocket,
        service: UserService = Provide[ApplicationContainer.service_container.user_service]
):
    try:
        await authorize_user(ws.headers, service)
    except KeyError:
        await ws.close(code=status.WS_1008_POLICY_VIOLATION, reason="unauthorized attempt connection")
    except:
        await ws.close(code=status.WS_1008_POLICY_VIOLATION, reason="token is invalid")
