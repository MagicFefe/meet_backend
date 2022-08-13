from functools import reduce
from typing import Callable
from files.file_manager import FileManager


class ListSaver:

    def __init__(
            self,
            file_manager: FileManager,
            saved_list_filename: str
    ):
        self.__file_manager = file_manager
        self.__saved_list_filename = saved_list_filename

    async def save_list(self, items: list[str]):
        meet_authors = ""
        if len(items) > 0:
            reducer: Callable[[str, str], str] = lambda initial, item: initial + f"{item} "
            meet_authors = reduce(reducer, items)
        file_exists = await self.__file_manager.file_exists(self.__saved_list_filename)
        if file_exists:
            await self.__file_manager.rewrite_file(self.__saved_list_filename, meet_authors)
        else:
            await self.__file_manager.write_or_create_file(self.__saved_list_filename, meet_authors)

    async def get_list(self) -> list[str]:
        file_exists = await self.__file_manager.file_exists(self.__saved_list_filename)
        if file_exists:
            predicate: Callable[[str], bool] = lambda item: len(item) > 0
            author_ids = await self.__file_manager.read_file(self.__saved_list_filename)
            return list(filter(predicate, author_ids.split(" ")))
        else:
            return []
