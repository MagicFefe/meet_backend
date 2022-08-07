from pydantic import BaseModel


class SignUp(BaseModel):
    name: str
    surname: str
    about: str
    dob: str
    gender: str
    email: str
    country: str
    city: str
    password: str
    image: str | None
