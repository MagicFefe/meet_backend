from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from db.enitites.base_class import Base
from uuid import uuid4


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    about = Column(String, nullable=False)
    dob = Column(String, nullable=False)
    email = Column(String, nullable=False)
    country = Column(String, nullable=False)
    city = Column(String, nullable=False)
    password = Column(String, nullable=False)
    image_filename = Column(String, nullable=False)
