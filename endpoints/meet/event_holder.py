from utils.data.observable_data import MutableObservableData


class Event:
    pass


class MeetAdded(Event):
    pass


class MeetDeleted(Event):
    pass


class Idle(Event):
    pass


class EventHolder:
    event: MutableObservableData[Event] = MutableObservableData(Idle())

    async def update_event(self, event: Event):
        await self.event.change_data(event)
