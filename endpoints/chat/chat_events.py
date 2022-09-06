class ChatListEvent:
    pass


class ChatDeleted(ChatListEvent):
    pass


class NewChatCreated(ChatListEvent):
    pass


class NewMessageInChatSent(ChatListEvent):
    pass


class Idle(ChatListEvent):
    pass
