from dependency_injector import containers, providers
from config import MEET_AUTHORS_FILENAME
from di.db_container import DbContainer
from di.file_storage_container import FileStorageContainer
from di.meet_container import MeetContainer
from di.repository_container import RepositoryContainer
from utils.saveable_list.list_saver import ListSaver
from utils.saveable_list.saveable_list import SaveableList


class ApplicationContainer(containers.DeclarativeContainer):
    db_container = providers.Container(
        DbContainer
    )

    file_storage_container = providers.Container(
        FileStorageContainer
    )

    list_saver = providers.Singleton(
        ListSaver,
        file_manager=file_storage_container.meet_authors_file_manager,
        saved_list_filename=MEET_AUTHORS_FILENAME
    )

    meet_authors_id_storage = providers.Singleton(
        SaveableList,
        items=[],
        list_saver=list_saver
    )

    meet_container = providers.Container(
        MeetContainer
    )

    repository_container = providers.Container(
        RepositoryContainer,
        meet_db=db_container.meet_db,
        db_session=db_container.db_session,
        user_image_file_manager=file_storage_container.user_image_file_manager
    )
