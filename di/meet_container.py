from dependency_injector import containers, providers
from config import MEET_AUTHORS_FILENAME
from endpoints.meet.meet_events import MeetEvent, Idle
from utils.event_holder.event_holder import EventHolder
from utils.saveable_list.list_saver import ListSaver
from utils.saveable_list.saveable_list import SaveableList


class MeetContainer(containers.DeclarativeContainer):
    meet_authors_file_manager = providers.Dependency()

    meet_event_holder = providers.Singleton(
        EventHolder[MeetEvent],
        default_value=Idle()
    )

    __list_saver = providers.Singleton(
        ListSaver,
        file_manager=meet_authors_file_manager,
        saved_list_filename=MEET_AUTHORS_FILENAME
    )

    meet_authors_id_storage = providers.Singleton(
        SaveableList,
        items=[],
        list_saver=__list_saver
    )
