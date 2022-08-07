from pydantic import BaseModel


class FeedbackAdd(BaseModel):
    user_id: str
    message: str
