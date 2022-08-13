from config import ANDROID_UPDATE_FILENAME, CURRENT_VERSION_UPDATE_FILE_FILENAME
from files.file_manager import FileManager


class UpdateRepository:
    def __init__(
            self,
            update_file_file_manager_android: FileManager
    ):
        self.__update_file_file_manager_android = update_file_file_manager_android

    async def get_update_file_path_android(self):
        file_path = ""
        file_exists = await self.__update_file_file_manager_android.file_exists(ANDROID_UPDATE_FILENAME)
        if file_exists:
            file_path = await self.__update_file_file_manager_android.full_storage_path + ANDROID_UPDATE_FILENAME
        return file_path

    async def get_current_version_android(self):
        current_version = ""
        file_exists = await self.__update_file_file_manager_android.file_exists(CURRENT_VERSION_UPDATE_FILE_FILENAME)
        if file_exists:
            current_version = \
                await self.__update_file_file_manager_android.read_file(CURRENT_VERSION_UPDATE_FILE_FILENAME)
        return current_version

    async def upload_update_file_android(self, update_file_bytes: bytes, update_file_version: str):
        update_file_exists = await self.__update_file_file_manager_android.file_exists(ANDROID_UPDATE_FILENAME)
        current_version_update_file_exists = await self.__update_file_file_manager_android.file_exists(
            CURRENT_VERSION_UPDATE_FILE_FILENAME
        )
        if not (update_file_exists or current_version_update_file_exists):
            await self.__update_file_file_manager_android.write_or_create_file_bytes(
                ANDROID_UPDATE_FILENAME,
                update_file_bytes
            )
            await self.__update_file_file_manager_android.write_or_create_file(
                CURRENT_VERSION_UPDATE_FILE_FILENAME,
                update_file_version
            )
        else:
            await self.__update_file_file_manager_android.rewrite_file_bytes(
                ANDROID_UPDATE_FILENAME,
                update_file_bytes
            )
            await self.__update_file_file_manager_android.rewrite_file(
                CURRENT_VERSION_UPDATE_FILE_FILENAME,
                update_file_version
            )
