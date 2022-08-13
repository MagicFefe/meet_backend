from repositories.update.update_repository import UpdateRepository


class UpdateService:
    def __init__(
            self,
            repository: UpdateRepository
    ):
        self.__repository = repository

    async def get_update_file_path_android(self):
        update_file_path = await self.__repository.get_update_file_path_android()
        return update_file_path

    async def get_current_version_android(self):
        current_version = await self.__repository.get_current_version_android()
        return current_version

    async def upload_update_file_android(self, update_file_bytes: bytes, update_file_version: str):
        await self.__repository.upload_update_file_android(update_file_bytes, update_file_version)
