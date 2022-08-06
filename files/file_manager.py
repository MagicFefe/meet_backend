from os import remove, path, makedirs
from exceptions import InvalidFilePathError


class FileManager:
    def __init__(
            self,
            storage_path: str
    ):
        if len(storage_path) == 0:
            raise InvalidFilePathError("storage path cannot be empty")
        if storage_path[0] != "/":
            if storage_path[len(storage_path)-1] != "/":
                self.full_storage_path = f"files/storage/{storage_path}/"
            else:
                self.full_storage_path = f"files/storage/{storage_path}"
        else:
            self.full_storage_path = f"files/storage{storage_path}"
        if not(path.exists(self.full_storage_path)):
            makedirs(self.full_storage_path, 0o666, exist_ok=True)

    def file_exists(self, file_name: str) -> bool:
        file_path = self.full_storage_path + file_name
        return path.exists(file_path)

    def write_or_create_file(self, file_name: str, data: str) -> str:
        file_path = self.full_storage_path + file_name
        with open(file_path, "w") as file:
            file.write(data)
        return file_name

    def write_or_create_file_bytes(self, file_name: str, data: bytes) -> str:
        file_path = self.full_storage_path + file_name
        with open(file_path, "wb") as new_file:
            new_file.write(data)
        return file_name

    def read_file(self, file_name: str) -> str:
        file_path = self.full_storage_path + file_name
        with open(file_path, "r") as file:
            data = file.read()
        return data

    def rewrite_file(self, file_name: str, data: str):
        file_path = self.full_storage_path + file_name
        with open(file_path, "r+") as file:
            file.truncate(0)
            file.seek(0)
            file.write(data)

    def rewrite_file_bytes(self, file_name: str, data: bytes):
        file_path = self.full_storage_path + file_name
        with open(file_path, "rb+") as file:
            file.truncate(0)
            file.seek(0)
            file.write(data)

    def delete_file(self, file_name: str):
        file_path = self.full_storage_path + file_name
        if self.file_exists(file_name):
            remove(file_path)
