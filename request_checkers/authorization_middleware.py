from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware
from repositories.user_repository import UserRepository
from fastapi.responses import JSONResponse
from utils.authorization_utils import authorize_user
from utils.request_utils import request_in_excluded

EXCLUDED_REQUESTS: dict[str, list] = {
    "/docs": ["GET"],
    "/openapi.json": ["GET"],
    "/sign_up": ["POST"],
    "/sign_in": ["POST"],
    "/feedback": ["GET"]
}


class AuthorizationMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            app,
            repository: UserRepository
    ):
        super().__init__(app)
        self.__repository: UserRepository = repository

    async def dispatch(self, request, call_next):
        if not(request_in_excluded(request, EXCLUDED_REQUESTS)):
            try:
                await authorize_user(request.headers, self.__repository)
            except KeyError:
                return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                                    content={"message": "unauthorized request"})
            except Exception:
                return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                    content={"message": "token is invalid"})
        response = await call_next(request)
        return response
