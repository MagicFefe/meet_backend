from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from db.enitites.base_class import Base
from uuid import uuid4


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String)
    surname = Column(String)
    email = Column(String)
    country = Column(String)
    city = Column(String)
    password = Column(String)
    image_path = Column(String)
