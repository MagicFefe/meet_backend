class UserAlreadyExistsError(Exception):
    pass


class MeetPointAlreadyExistsError(Exception):
    pass


class ExceptionWithDetail(Exception):
    def __init__(self, detail: str):
        self.detail = detail


class InvalidImageError(ExceptionWithDetail):
    pass


class InvalidFilePathError(ExceptionWithDetail):
    pass
