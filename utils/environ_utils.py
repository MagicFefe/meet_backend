from os import environ


def get_or_default(__key, default):
    value = environ.get(__key)
    if value is None:
        return default
    else:
        return value
