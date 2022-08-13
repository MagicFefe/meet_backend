from json import loads
from typing import Mapping
from jwcrypto.jwk import JWK
from jwcrypto.jwt import JWT
from config import JWK_KEY, JWK_TYPE
from exceptions import UserDoesNotExistError
from services.user.user_service import UserService


async def authorize_user(
        headers: Mapping[str, str],
        user_service: UserService
):
    token = headers["Authorization"]
    key = JWK(k=JWK_KEY, kty=JWK_TYPE)
    raw_jwt = JWT(jwt=token, key=key)
    data: dict[str, str] = loads(raw_jwt.claims)
    email: str = data["email"]
    user_db = await user_service.get_user_by_email(email)
    if user_db is None:
        return UserDoesNotExistError()
