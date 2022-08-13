from models.feedback.feedback_add import FeedbackAdd
from repositories.feedback.feedback_repository import FeedbackRepository


class FeedbackService:
    def __init__(
            self,
            repository: FeedbackRepository
    ):
        self.__repository = repository

    async def add_feedback(self, new_feedback: FeedbackAdd):
        await self.__repository.add_feedback(new_feedback)

    async def get_all_feedbacks(self):
        feedbacks = await self.__repository.get_all_feedbacks()
        return feedbacks
