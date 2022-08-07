from pydantic import BaseModel


class FeedbackResponse(BaseModel):
    id: str
    user_id: str
    message: str
