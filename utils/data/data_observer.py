from typing import Callable, TypeVar, Generic, Optional, Coroutine

T = TypeVar("T")


class DataObserver(Generic[T]):
    def __init__(self, on_next: Callable[[T], Coroutine], on_error: Optional[Callable[[], None]] = None):
        self.on_next = on_next
        self.on_error = on_error
