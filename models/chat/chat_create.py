from pydantic import BaseModel


class ChatCreate(BaseModel):
    users: list[str]
