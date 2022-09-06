from datetime import datetime
from config import DATETIME_PATTERN
from db.enitites.message.message import Message
from models.message.message_response import MessageResponse


def from_message_to_message_response(message_db: Message) -> MessageResponse:
    return MessageResponse(
        id=str(message_db.id),
        text=message_db.text,
        user_id=str(message_db.user_id),
        chat_id=str(message_db.chat_id),
        send_date=datetime.strftime(message_db.send_date, DATETIME_PATTERN),
    )
