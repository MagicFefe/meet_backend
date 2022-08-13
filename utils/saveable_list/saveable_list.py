from utils.saveable_list.list_saver import ListSaver


class SaveableList:

    def __init__(
            self,
            items: list[str],
            list_saver: ListSaver
    ):
        self.items = items
        self.__list_saver = list_saver

    async def on_save(self):
        await self.__list_saver.save_list(self.items)

    async def on_restore(self):
        self.items = await self.__list_saver.get_list()
