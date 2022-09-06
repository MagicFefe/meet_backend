from pydantic import BaseModel


class MessageSend(BaseModel):
    text: str
