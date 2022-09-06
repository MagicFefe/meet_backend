from uuid import uuid4
from sqlalchemy import Column, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from db.enitites.base_class import Base


class UserChatAssociation(Base):
    __tablename__ = "user_chat_association"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True, default=uuid4)
    chat_id = Column(UUID(as_uuid=True), ForeignKey("chats.id"), primary_key=True, default=uuid4)
    last_read_message_date = Column(DateTime, nullable=True)
