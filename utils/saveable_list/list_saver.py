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

    def save_list(self, items: list[str]):
        if len(items) > 0:
            reducer: Callable[[str, str], str] = lambda initial, item: initial + f"{item} "
            meet_authors = reduce(reducer, items)
            if self.__file_manager.file_exists(self.__saved_list_filename):
                self.__file_manager.rewrite_file(self.__saved_list_filename, meet_authors)
            else:
                self.__file_manager.write_or_create_file(self.__saved_list_filename, meet_authors)
        else:
            if self.__file_manager.file_exists(self.__saved_list_filename):
                self.__file_manager.rewrite_file(self.__saved_list_filename, "")
            else:
                self.__file_manager.write_or_create_file(self.__saved_list_filename, "")

    def get_list(self) -> list[str]:
        if self.__file_manager.file_exists(self.__saved_list_filename):
            predicate: Callable[[str], bool] = lambda item: len(item) > 0
            return list(filter(predicate, self.__file_manager.read_file(self.__saved_list_filename).split(" ")))
        else:
            return []
