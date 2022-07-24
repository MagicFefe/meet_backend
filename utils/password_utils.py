from config import ENCODING
from hashlib import sha512, sha256


def gen_salt(email: str) -> bytes:
    return sha256(email.encode(ENCODING)).hexdigest().encode(ENCODING)


def get_hashed_password(password: str, email: str) -> str:
    salt = gen_salt(email)
    return sha512(password.encode(ENCODING)+salt).hexdigest()
