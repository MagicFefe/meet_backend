from dependency_injector import containers, providers

from repositories.feedback_repository import FeedbackRepository
from repositories.meet_repository import MeetRepository
from repositories.user_repository import UserRepository


class RepositoryContainer(containers.DeclarativeContainer):
    meet_db = providers.Dependency()
    db_session = providers.Dependency()
    user_image_file_manager = providers.Dependency()

    meet_repository = providers.Singleton(
        MeetRepository,
        meet_db=meet_db
    )

    user_repository = providers.Singleton(
        UserRepository,
        db_session=db_session,
        user_image_file_manager=user_image_file_manager
    )

    feedback_repository = providers.Singleton(
        FeedbackRepository,
        db_session=db_session
    )
