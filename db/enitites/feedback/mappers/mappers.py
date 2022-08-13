from db.enitites.feedback.feedback import Feedback
from models.feedback.feedback_response import FeedbackResponse


def from_feedback_to_feedback_response(feedback: Feedback) -> FeedbackResponse:
    return FeedbackResponse(
        id=str(feedback.id),
        user_id=str(feedback.user_id),
        message=feedback.message
    )
