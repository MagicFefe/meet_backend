from db.enitites.feedback.feedback import Feedback
from models.feedback.feedback_add import FeedbackAdd


def from_feedback_add_to_feedback(feedback_add: FeedbackAdd) -> Feedback:
    feedback = Feedback()
    feedback.user_id = feedback_add.user_id
    feedback.message = feedback_add.message
    return feedback
