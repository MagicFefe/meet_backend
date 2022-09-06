from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from config import NON_AUTH_REQUESTS
from services.user.user_service import UserService
from utils.authorization_utils import authorize_user
from utils.request_utils import request_in_excluded


class AuthorizationMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            app,
            service: UserService
    ):
        super().__init__(app)
        self.__service: UserService = service

    async def dispatch(self, request, call_next):
        if not (request_in_excluded(request, NON_AUTH_REQUESTS)):
            try:
                await authorize_user(request.headers, self.__service)
            except KeyError:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED, content={"message": "unauthorized request"}
                )
            except:
                return JSONResponse(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"message": "token is invalid"}
                )
        response = await call_next(request)
        return response
