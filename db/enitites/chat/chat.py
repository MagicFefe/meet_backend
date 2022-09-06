from uuid import uuid4
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.enitites.base_class import Base
from db.enitites.user_chat_assoc.user_chat_assoc import UserChatAssociation
from utils.import_resolvers import resolve_message_model


class Chat(Base):
    __tablename__ = "chats"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    chat_name = Column(String, default=None)
    last_activity_date = Column(DateTime, nullable=False)
    users = relationship(
        "User",
        back_populates="chats",
        secondary="user_chat_association",
        primaryjoin=lambda: Chat.id == UserChatAssociation.chat_id,
        lazy="subquery",
        passive_deletes=True
    )
    messages = relationship(
        resolve_message_model(),
        primaryjoin=lambda: Chat.id == resolve_message_model().chat_id,
        lazy="noload",
        cascade="all, delete"
    )
