from sqlalchemy import Column, String, Integer
from db.enitites.base_class import Base


class User(Base, object):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    surname = Column(String)
    email = Column(String)
    country = Column(String)
    city = Column(String)
    password = Column(String)
