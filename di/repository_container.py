from dependency_injector import containers, providers

from repositories.feedback.feedback_repository import FeedbackRepository
from repositories.meet.meet_repository import MeetRepository
from repositories.update.update_repository import UpdateRepository
from repositories.user.user_repository import UserRepository


class RepositoryContainer(containers.DeclarativeContainer):
    meet_db = providers.Dependency()
    db_session = providers.Dependency()
    user_image_file_manager = providers.Dependency()
    meet_authors_id_storage = providers.Dependency()
    update_file_file_manager_android = providers.Dependency()

    meet_repository = providers.Singleton(
        MeetRepository,
        meet_db=meet_db,
        meet_authors_id_storage=meet_authors_id_storage
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

    update_repository = providers.Singleton(
        UpdateRepository,
        update_file_file_manager_android=update_file_file_manager_android
    )
