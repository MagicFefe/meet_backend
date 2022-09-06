from typing import Callable, Any, Coroutine
from fastapi import HTTPException
from fastapi.openapi.models import Response
from fastapi.routing import APIRoute
from starlette import status
from starlette.requests import Request
from config import ADMIN_SECRET, ADMIN_REQUESTS
from utils.request_utils import request_in_excluded


class AdminRightsRoute(APIRoute):
    def get_route_handler(self) -> Callable[[Request], Coroutine[Any, Any, Response]]:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request):
            if request_in_excluded(request, ADMIN_REQUESTS):
                secret_key = request.headers.get("admin-secret", None)
                if secret_key is None:
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="unauthorized request")
                if secret_key != ADMIN_SECRET:
                    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="invalid key")
            return await original_route_handler(request)

        return custom_route_handler
