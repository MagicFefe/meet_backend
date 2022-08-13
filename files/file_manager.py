from os import path, makedirs
from aiofiles.os import remove
from aiofiles import open
from aiofiles.ospath import exists
from exceptions import InvalidFilePathError


class FileManager:
    def __init__(
            self,
            storage_path: str
    ):
        if len(storage_path) == 0:
            raise InvalidFilePathError("storage path cannot be empty")
        if storage_path[0] != "/":
            if storage_path[len(storage_path) - 1] != "/":
                self.full_storage_path = f"files/storage/{storage_path}/"
            else:
                self.full_storage_path = f"files/storage/{storage_path}"
        else:
            self.full_storage_path = f"files/storage{storage_path}"
        if not (path.exists(self.full_storage_path)):
            makedirs(self.full_storage_path, 0o666, exist_ok=True)

    async def file_exists(self, file_name: str) -> bool:
        file_path = self.full_storage_path + file_name
        file_exists = await exists(file_path)
        return file_exists

    async def write_or_create_file(self, file_name: str, data: str) -> str:
        file_path = self.full_storage_path + file_name
        async with open(file_path, "w") as file:
            await file.write(data)
        return file_name

    async def write_or_create_file_bytes(self, file_name: str, data: bytes) -> str:
        file_path = self.full_storage_path + file_name
        async with open(file_path, "wb") as new_file:
            await new_file.write(data)
        return file_name

    async def read_file(self, file_name: str) -> str:
        file_path = self.full_storage_path + file_name
        async with open(file_path, "r") as file:
            data = await file.read()
        return data

    async def rewrite_file(self, file_name: str, data: str):
        file_path = self.full_storage_path + file_name
        async with open(file_path, "r+") as file:
            await file.truncate(0)
            await file.seek(0)
            await file.write(data)

    async def rewrite_file_bytes(self, file_name: str, data: bytes):
        file_path = self.full_storage_path + file_name
        async with open(file_path, "rb+") as file:
            await file.truncate(0)
            await file.seek(0)
            await file.write(data)

    async def delete_file(self, file_name: str):
        file_path = self.full_storage_path + file_name
        file_exists = await self.file_exists(file_name)
        if file_exists:
            await remove(file_path)
