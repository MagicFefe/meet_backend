from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from services.user.user_service import UserService
from utils.authorization_utils import authorize_user
from utils.request_utils import request_in_excluded

EXCLUDED_REQUESTS: dict[str, list] = {
    "/docs": ["GET"],
    "/openapi.json": ["GET"],
    "/sign_up": ["POST"],
    "/sign_in": ["POST"],
    "/feedback": ["GET"],
    "/update": ["POST"]
}


class AuthorizationMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            app,
            service: UserService
    ):
        super().__init__(app)
        self.__service: UserService = service

    async def dispatch(self, request, call_next):
        if not(request_in_excluded(request, EXCLUDED_REQUESTS)):
            try:
                await authorize_user(request.headers, self.__service)
            except KeyError:
                return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                                    content={"message": "unauthorized request"})
            except Exception:
                return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                    content={"message": "token is invalid"})
        response = await call_next(request)
        return response
