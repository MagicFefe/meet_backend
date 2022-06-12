from pydantic import BaseModel


class UserRegister(BaseModel):
    name: str
    surname: str
    email: str
    country: str
    city: str
    password: str
