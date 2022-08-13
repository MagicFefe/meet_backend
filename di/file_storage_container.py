from dependency_injector import containers, providers
from config import USER_IMAGE_FILE_STORAGE_PATH, UPDATE_FILE_STORAGE_PATH, MEET_AUTHORS_FILE_STORAGE_PATH, \
    ANDROID_CLIENT_PLATFORM_NAME
from files.file_manager import FileManager


class FileStorageContainer(containers.DeclarativeContainer):
    user_image_file_manager = providers.Singleton(
        FileManager,
        storage_path=USER_IMAGE_FILE_STORAGE_PATH
    )

    meet_authors_file_manager = providers.Singleton(
        FileManager,
        storage_path=MEET_AUTHORS_FILE_STORAGE_PATH
    )

    update_file_file_manager_android = providers.Singleton(
        FileManager,
        storage_path=UPDATE_FILE_STORAGE_PATH + ANDROID_CLIENT_PLATFORM_NAME + "/"
    )
