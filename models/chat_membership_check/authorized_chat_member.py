from pydantic import BaseModel


class AuthorizedChatMember(BaseModel):
    chat_id: str
    user_id: str
