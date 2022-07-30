from pydantic import BaseModel


class MeetDelete(BaseModel):
    id: str
    author_id: str
