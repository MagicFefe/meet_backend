from pydantic import BaseModel


class MeetResponse(BaseModel):
    id: str
    author_id: str
    meet_name: str
    meet_description: str
    latitude: float
    longitude: float
    created_at: str
