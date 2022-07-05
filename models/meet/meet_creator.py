from pydantic import BaseModel


class MeetCreator(BaseModel):
    author_id: str
    author_name: str
    author_surname: str
