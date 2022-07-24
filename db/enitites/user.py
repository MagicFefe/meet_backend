from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from db.enitites.base_class import Base
from uuid import uuid4

"""
 An [image] represented in DB as base64 encoded bytes 
"""


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String)
    surname = Column(String)
    email = Column(String)
    country = Column(String)
    city = Column(String)
    password = Column(String)
    image = Column(String)
