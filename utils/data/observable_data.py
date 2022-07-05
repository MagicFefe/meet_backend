from typing import Generic, TypeVar
from .data_observer import DataObserver

T = TypeVar("T")


class ObservableData(Generic[T]):
    _observers: dict[int, DataObserver] = {}
    data: T

    def __init__(self, data: T):
        self.data = data

    async def subscribe(self, observer: DataObserver[T]):
        object_hash = observer.__hash__()
        if not (object_hash in self._observers.keys()):
            self._observers[object_hash] = observer
            await observer.on_next(self.data)

    def unsubscribe(self, observer: DataObserver[T]):
        try:
            self._observers.pop(observer.__hash__())
        except KeyError:
            return

    def __exit__(self, exc_type, exc_val, exc_tb):
        for key in self._observers:
            self._observers.pop(key)


class MutableObservableData(Generic[T], ObservableData[T]):
    def __init__(self, data: T):
        super().__init__(data)

    async def __notify(self, new_data: T):
        observers = self._observers
        for key in observers:
            await observers[key].on_next(new_data)

    async def change_data(self, new_data: T):
        self.data = new_data
        await self.__notify(new_data)
