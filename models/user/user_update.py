from pydantic import BaseModel


class UserUpdate(BaseModel):
    id: str
    name: str
    surname: str
    about: str
    dob: str
    email: str
    country: str
    city: str
    image: str
    old_password: str
    new_password: str
