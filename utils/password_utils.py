from os import urandom
from config import ENCODING
from hashlib import sha512


def get_hashed_password(password: str) -> str:
    salt = urandom(32)
    return sha512(password.encode(ENCODING)+salt).hexdigest()
