from starlette.requests import Request


def request_in_excluded(request: Request, excluded: dict[str, list[str]]) -> bool:
    return any(
        admin_request_path in request.scope["path"] and request.method in admin_request_methods
        for admin_request_path, admin_request_methods in excluded.items()
    )
