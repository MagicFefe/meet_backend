from dependency_injector.wiring import inject, Provide
from starlette import status
from starlette.websockets import WebSocket
from di.application_container import ApplicationContainer
from repositories.user_repository import UserRepository
from utils.authorization_utils import authorize_user


@inject
async def check_ws_header(
        ws: WebSocket,
        user_repository: UserRepository = Provide[ApplicationContainer.repository_container.user_repository]
):
    try:
        await authorize_user(ws.headers, user_repository)
    except KeyError:
        await ws.close(code=status.WS_1008_POLICY_VIOLATION, reason="unauthorized attempt connection")
    except:
        await ws.close(code=status.WS_1008_POLICY_VIOLATION, reason="token is invalid")
