from pydantic import BaseModel


class UserRegister(BaseModel):
    name: str
    surname: str
    about: str
    dob: str
    email: str
    country: str
    city: str
    password: str
    image: str | None
