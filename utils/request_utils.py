from starlette.requests import Request


def request_in_excluded(request: Request, excluded: dict[str, list[str]]) -> bool:
    return any(
        request_path in request.scope["path"] and request.method in request_methods
        for request_path, request_methods in excluded.items()
    )
