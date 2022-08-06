def first_version_is_lower(first_version: str, second_version: str) -> bool:
    first_version_list = list[str](first_version.split("."))
    second_version_list = list[str](filter(str.isdigit, second_version.split(".")))
    return any(
        int(current) < int(uploading)
        for current, uploading in zip(first_version_list, second_version_list)
    )
