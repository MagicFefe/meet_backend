from config import ENCODING
from hashlib import sha512, sha256


def get_hashed_password(password: str, email: str, name: str, surname: str) -> str:
    salt = sha256((email + " " + name + " " + surname).encode(ENCODING)).hexdigest().encode(ENCODING)
    return sha512(password.encode(ENCODING)+salt).hexdigest()
