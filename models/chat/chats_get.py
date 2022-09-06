from pydantic import BaseModel


class ChatsGet(BaseModel):
    chats: list[str]
    user_id: str
