from pydantic import BaseModel


class ChatResponse(BaseModel):
    id: str
    chat_name: str | None
    users: list
