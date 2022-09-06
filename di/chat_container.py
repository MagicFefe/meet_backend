from dependency_injector import containers, providers
from endpoints.chat.chat_events import ChatListEvent, Idle
from utils.event_holder.event_holder import EventHolder
from utils.ws_connectivity_manager.ws_connectivity_manager import WSConnectivityManager


class ChatContainer(containers.DeclarativeContainer):
    chat_connections_manager = providers.Singleton(
        WSConnectivityManager
    )

    chat_list_connections_manager = providers.Singleton(
        WSConnectivityManager
    )

    chat_list_event_holder = providers.Singleton(
        EventHolder[ChatListEvent],
        default_value=Idle()
    )
