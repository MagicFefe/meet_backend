from pydantic import BaseModel


class UserResponse(BaseModel):
    name: str
    surname: str
    email: str
    country: str
    city: str
    jwt: str
