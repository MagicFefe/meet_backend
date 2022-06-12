from pydantic import BaseModel


class UserMinimal(BaseModel):
    email: str
    password: str
