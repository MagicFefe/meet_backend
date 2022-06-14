from fastapi import Depends
from dependencies import get_session, get_user_repository
from starlette.middleware.base import BaseHTTPMiddleware
from jwcrypto.jwk import JWK
from jwcrypto.jwt import JWT
from json import loads
from config import JWK, JWK_TYPE
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.user_repository import UserRepository
from fastapi.responses import JSONResponse

excluded_requests: dict[str, list] = {
    "/api/user": ["POST", "GET"],
    "/docs": ["GET"],
    "/openapi.json": ["GET"]
}


class AuthorizationMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            app,
            session=Depends(get_session),
            repository: UserRepository = Depends(get_user_repository)
    ):
        super().__init__(app)
        self.session: AsyncSession = session
        self.repository = repository

    async def dispatch(self, request, call_next):
        for excluded_request_path in excluded_requests:
            excluded_request_methods = excluded_requests[excluded_request_path]
            if request.method in excluded_request_methods and excluded_request_path in request.scope["path"]:
                response = await call_next(request)
                return response
        try:
            token = request.headers["Authorization"]
        except KeyError:
            return JSONResponse(status_code=401, content={"message": "unauthorized request"})
        try:
            key = JWK(k=JWK, kty=JWK_TYPE)
            raw_jwt = JWT(jwt=token, key=key)
            data: dict[str, str] = loads(raw_jwt.claims)
            email: str = data["email"]
        except:
            return JSONResponse(status_code=422, content={"message": "token is invalid"})
        async with self.session.begin():
            user_db = await self.repository.get_user_by_email(self.session, email)
        if user_db is None:
            return JSONResponse(status_code=401, content={"message": "unauthorized request"})
        response = await call_next(request)
        return response
