from dependency_injector import containers, providers

from repositories.meet_repository import MeetRepository
from repositories.user_repository import UserRepository


class RepositoryContainer(containers.DeclarativeContainer):
    meet_db = providers.Dependency()
    user_db_session = providers.Dependency()
    user_image_file_manager = providers.Dependency()

    meet_repository = providers.Singleton(
        MeetRepository,
        meet_db=meet_db
    )

    user_repository = providers.Singleton(
        UserRepository,
        user_db_session=user_db_session,
        user_image_file_manager=user_image_file_manager
    )
