from pydantic import BaseModel


class ChatDelete(BaseModel):
    user_id: str
    chat_id: str
