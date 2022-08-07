from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db.enitites.feedback.feedback import Feedback
from models.feedback.feedback_add import FeedbackAdd
from models.feedback.feedback_response import FeedbackResponse


class FeedbackRepository:

    def __init__(
            self,
            db_session: AsyncSession
    ):
        self.__db_session = db_session

    async def add_feedback(self, new_feedback: FeedbackAdd):
        async with self.__db_session:
            self.__db_session.add(
                from_feedback_add_to_feedback(new_feedback)
            )
            await self.__db_session.commit()

    async def get_all_feedbacks(self):
        result = await self.__db_session.execute(select(Feedback))
        return result.scalars()


def from_feedback_add_to_feedback(feedback_add: FeedbackAdd) -> Feedback:
    feedback = Feedback()
    feedback.user_id = feedback_add.user_id
    feedback.message = feedback_add.message
    return feedback


def from_feedback_to_feedback_response(feedback: Feedback) -> FeedbackResponse:
    return FeedbackResponse(
        id=str(feedback.id),
        user_id=str(feedback.user_id),
        message=feedback.message
    )
