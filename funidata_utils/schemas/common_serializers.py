from typing import Iterable


def serialize_as_list[typevar](v: set[typevar] | list[typevar] | None) -> list[typevar] | None:
    if v is None:
        return None

    try:
        return list(set(v))
    except Exception as e:
        # If it can't be hashed to set, just return as list
        return list(v)
