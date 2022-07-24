from jwcrypto.jwk import JWK
from jwcrypto.jwt import JWT
from config import JWK_KEY as SECRET
from config import JWK_TYPE
from config import JWT_ALG
from config import JWT_NAME


def generate_jwt(payload: dict[str, str]) -> JWT:
    key = JWK(k=SECRET, kty=JWK_TYPE)
    token = JWT(
        header={
            "alg": JWT_ALG,
            "typ": JWT_NAME
        },
        claims=payload
    )
    token.make_signed_token(key)
    token.serialize()
    return token
