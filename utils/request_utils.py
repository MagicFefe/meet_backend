from starlette.requests import Request


def request_in_excluded(request: Request, excluded: dict[str, list[str]]) -> bool:
    return any(
        excluded_request_path in request.scope["path"] and request.method in excluded_request_methods
        for excluded_request_path, excluded_request_methods in excluded.items()
    )
