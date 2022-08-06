from dependency_injector import containers, providers
from endpoints.meet.event_holder import EventHolder


class MeetContainer(containers.DeclarativeContainer):
    event_holder = providers.Singleton(
        EventHolder
    )
