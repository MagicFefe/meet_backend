from pydantic import BaseModel


class MeetUpdate(BaseModel):
    id: str
    meet_name: str
    meet_description: str
