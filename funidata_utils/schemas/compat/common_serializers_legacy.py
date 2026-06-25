from typing import TypeVar


T = TypeVar('T')


def serialize_as_list(v: set[T] | list[T] | None) -> list[T] | None:
    if v is None:
        return None

    try:
        return list(set(v))
    except Exception as e:
        # If it can't be hashed to set, just return as list
        return list(v)
