from db.enitites.chat.chat import Chat
from models.chat.chat_response import ChatResponse


def from_chat_to_chat_response(chat: Chat) -> ChatResponse:
    users_response = [str(user.id) for user in chat.users]

    return ChatResponse(
        id=str(chat.id),
        chat_name=chat.chat_name,
        users=users_response
    )
