from utils.saveable_list.list_saver import ListSaver


class SaveableList:

    def __init__(
            self,
            items: list[str],
            list_saver: ListSaver
    ):
        self.items = items
        self.__list_saver = list_saver

    def on_save(self):
        self.__list_saver.save_list(self.items)

    def on_restore(self):
        self.items = self.__list_saver.get_list()
