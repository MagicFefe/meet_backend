from pydantic import BaseModel


class UserResponse(BaseModel):
    id: str
    name: str
    surname: str
    about: str
    dob: str
    gender: str
    email: str
    country: str
    city: str
    image: str


class UserResponseWithToken(UserResponse):
    jwt: str
