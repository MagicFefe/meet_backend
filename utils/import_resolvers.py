
def resolve_message_model():
    from db.enitites.message.message import Message
    return Message


def resolve_user_chat_association_model():
    from db.enitites.user_chat_assoc.user_chat_assoc import UserChatAssociation
    return UserChatAssociation


def resolve_chat_model():
    from db.enitites.chat.chat import Chat
    return Chat
