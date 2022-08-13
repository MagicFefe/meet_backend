from typing import AsyncIterator, Callable
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db.enitites.feedback.feedback import Feedback
from models.feedback.feedback_add import FeedbackAdd
from models.feedback.mappers.mappers import from_feedback_add_to_feedback


class FeedbackRepository:

    def __init__(
            self,
            db_session: Callable[[], AsyncIterator[AsyncSession]]
    ):
        self.__db_session = db_session

    async def add_feedback(self, new_feedback: FeedbackAdd):
        async with self.__db_session() as session:
            session.add(
                from_feedback_add_to_feedback(new_feedback)
            )
            await session.commit()

    async def get_all_feedbacks(self):
        async with self.__db_session() as session:
            result = await session.execute(select(Feedback))
            return result.scalars()
