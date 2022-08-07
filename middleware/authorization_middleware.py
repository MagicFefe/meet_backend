from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware
from jwcrypto.jwk import JWK
from jwcrypto.jwt import JWT
from json import loads
from config import JWK_KEY, JWK_TYPE
from repositories.user_repository import UserRepository
from fastapi.responses import JSONResponse
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
                token = request.headers["Authorization"]
            except KeyError:
                return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message": "unauthorized request"})
            try:
                key = JWK(k=JWK_KEY, kty=JWK_TYPE)
                raw_jwt = JWT(jwt=token, key=key)
                data: dict[str, str] = loads(raw_jwt.claims)
                email: str = data["email"]
            except:
                return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                    content={"message": "token is invalid"})
            user_db = await self.__repository.get_user_by_email(email)
            if user_db is None:
                return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message": "unauthorized request"})
        response = await call_next(request)
        return response
