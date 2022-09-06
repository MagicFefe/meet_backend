from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.enitites.base_class import Base
from uuid import uuid4
from db.enitites.user_chat_assoc.user_chat_assoc import UserChatAssociation
from utils.import_resolvers import resolve_chat_model


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    about = Column(String, nullable=False)
    dob = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    email = Column(String, nullable=False)
    country = Column(String, nullable=False)
    city = Column(String, nullable=False)
    password = Column(String, nullable=False)
    image_filename = Column(String, nullable=False)
    deleted = Column(Boolean, nullable=False, default=False)
    chats = relationship(
        resolve_chat_model(),
        back_populates="users",
        secondary="user_chat_association",
        primaryjoin=lambda: User.id == UserChatAssociation.user_id,
        lazy="subquery",
        cascade="all, delete"
    )
