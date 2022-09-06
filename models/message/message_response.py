from pydantic import BaseModel


class MessageResponse(BaseModel):
    id: str
    text: str
    user_id: str
    chat_id: str
    send_date: str
