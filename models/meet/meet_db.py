from pydantic import BaseModel
from uuid import UUID


class MeetDB(BaseModel):
    id: str
    author_id: str
    meet_name: str
    meet_description: str
    author_name: str
    author_surname: str
    created_at: str
