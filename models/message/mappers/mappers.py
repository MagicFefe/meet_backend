from datetime import datetime
from uuid import UUID

from models.message.message_send import MessageSend
from db.enitites.message.message import Message


def from_message_send_to_message(
        message_send: MessageSend, chat_id: UUID, user_id: UUID, current_date: datetime
) -> Message:
    message_db = Message()
    message_db.text = message_send.text
    message_db.user_id = user_id
    message_db.chat_id = chat_id
    message_db.send_date = current_date
    return message_db
