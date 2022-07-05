from pydantic import BaseModel
from .meet_creator import MeetCreator


class Meet(BaseModel):
    meet_name: str
    meet_description: str
    author: MeetCreator
