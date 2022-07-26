from pydantic import BaseModel


class UserUpdate(BaseModel):
    id: str
    name: str
    surname: str
    new_email: str
    old_email: str
    country: str
    city: str
    image: str
    old_password: str
    new_password: str
