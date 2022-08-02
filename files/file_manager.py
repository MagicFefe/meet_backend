from os import mkdir, remove, path
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
            mkdir(self.full_storage_path, 0o666)

    def write_or_create_file(self, file_name: str, data: str) -> str:
        file_path = self.full_storage_path + file_name
        with open(file_path, "w") as file:
            file.write(data)
        return file_name

    def read_file(self, file_name: str) -> str:
        file_path = self.full_storage_path + file_name
        with open(file_path, "r") as file:
            data = file.read()
        return data

    def delete_file(self, file_name: str):
        file_path = self.full_storage_path + file_name
        if path.exists(file_path):
            remove(file_path)
