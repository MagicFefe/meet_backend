from pydantic import BaseModel


class MeetResponseDetails(BaseModel):
    id: str
    author_id: str
    author_name: str
    author_surname: str
    author_image: str
    meet_name: str
    meet_description: str
    latitude: float
    longitude: float
    created_at: str
