from dependency_injector import containers, providers

from services.chat.chat_service import ChatService
from services.feedback.feedback_service import FeedbackService
from services.meet.meet_service import MeetService
from services.message.message_service import MessageService
from services.update.update_service import UpdateService
from services.user.user_service import UserService


class ServiceContainer(containers.DeclarativeContainer):
    user_repository = providers.Dependency()
    meet_repository = providers.Dependency()
    feedback_repository = providers.Dependency()
    update_repository = providers.Dependency()
    chat_repository = providers.Dependency()
    message_repository = providers.Dependency()

    user_service = providers.Singleton(
        UserService,
        repository=user_repository
    )

    meet_service = providers.Singleton(
        MeetService,
        repository=meet_repository
    )

    feedback_service = providers.Singleton(
        FeedbackService,
        repository=feedback_repository
    )

    update_service = providers.Singleton(
        UpdateService,
        repository=update_repository
    )

    chat_service = providers.Singleton(
        ChatService,
        repository=chat_repository
    )

    message_service = providers.Singleton(
        MessageService,
        repository=message_repository
    )
