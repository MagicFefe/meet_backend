from typing import TypeVar, Generic
from utils.observable_data.observable_data import MutableObservableData

T = TypeVar("T")


class EventHolder(Generic[T]):

    def __init__(
            self,
            default_value: T
    ):
        self.__default_value = default_value
        self.event: MutableObservableData[T] = MutableObservableData(self.__default_value)

    async def update_event(self, event: T):
        await self.event.change_data(event)
