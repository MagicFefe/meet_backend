from pydantic import BaseModel


class Meet(BaseModel):
    meet_name: str
    meet_description: str
    author_id: str
    author_name: str
    author_surname: str
    latitude: float
    longitude: float
