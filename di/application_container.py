from dependency_injector import containers, providers
from di.chat_container import ChatContainer
from di.db_container import DbContainer
from di.file_storage_container import FileStorageContainer
from di.meet_container import MeetContainer
from di.repository_container import RepositoryContainer
from di.service_container import ServiceContainer


class ApplicationContainer(containers.DeclarativeContainer):
    db_container = providers.Container(
        DbContainer
    )

    file_storage_container = providers.Container(
        FileStorageContainer
    )

    meet_container = providers.Container(
        MeetContainer,
        meet_authors_file_manager=file_storage_container.meet_authors_file_manager
    )

    chat_container = providers.Container(
        ChatContainer
    )

    repository_container = providers.Container(
        RepositoryContainer,
        meet_db=db_container.meet_db,
        db_session=db_container.db.provided.get_session,
        user_image_file_manager=file_storage_container.user_image_file_manager,
        meet_authors_id_storage=meet_container.meet_authors_id_storage,
        update_file_file_manager_android=file_storage_container.update_file_file_manager_android
    )

    service_container = providers.Container(
        ServiceContainer,
        user_repository=repository_container.user_repository,
        meet_repository=repository_container.meet_repository,
        feedback_repository=repository_container.feedback_repository,
        update_repository=repository_container.update_repository,
        chat_repository=repository_container.chat_repository,
        message_repository=repository_container.message_repository
    )
