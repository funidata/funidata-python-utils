#  Copyright (c) 2025 Funidata Oy.
#  All rights reserved.
# ------------------------------------------------------------------------------
import sys
import typing
from collections import defaultdict
from functools import reduce
from statistics import mean, stdev
from typing import Any, Generator, Callable, Literal, Tuple

import httpx


if sys.version_info >= (3, 12):
    from .compat.utils_312 import group_by  # noqa: F401 ("Unused import")
else:
    from .compat.utils_legacy import group_by  # noqa: F401 ("Unused import")


def _recursive_flatten(
    lst: list
) -> Generator:
    for i in lst:
        if isinstance(i, list):
            for j in _recursive_flatten(i):
                yield j
        else:
            yield i


def flatten(
    lst: list
) -> list:
    return list(_recursive_flatten(lst))


def group_indexes_by(
    seq: list,
    key: Callable
) -> dict[Any, list[int]]:
    return reduce(
        lambda grp, val: grp[key(val[1])].append(val[0]) or grp,
        enumerate(seq),
        defaultdict(list)
    )


def response_statistics(
    data: list[httpx.Response],
    resolution_digits: int = 4
) -> dict:
    def _prty(val: float):
        return f'{val:.{resolution_digits}f}s'

    _avg = mean([x.elapsed.total_seconds() for x in data])
    _std = stdev([x.elapsed.total_seconds() for x in data]) if len(data) >= 2 else None
    _sum = sum(([x.elapsed.total_seconds() for x in data]))
    _max = max([x.elapsed.total_seconds() for x in data])
    _min = min([x.elapsed.total_seconds() for x in data])
    return {
        'total': _prty(_sum),
        'average': _prty(_avg),
        'stdev': _prty(_std),
        'min': _prty(_min),
        'max': _prty(_max),
    }


def batch(iterable, steps=1):
    length = len(iterable)
    for index in range(0, length, steps):
        yield iterable[index:min(index + steps, length)]


def recursive_dict_fetch(
    entity: Any,
    keys: list,
    missing_key_handler: typing.Literal['skip', 'exception'] = 'exception',
):
    if not entity:
        return None

    if len(keys) == 1:
        if isinstance(entity, list):
            return entity

        if keys[0] not in entity:
            match missing_key_handler:
                case 'skip':
                    return None
                case 'exception' | _:
                    raise KeyError(f"Could not find {keys[0]} in entity")

        return entity[keys[0]]

    return recursive_dict_fetch(entity[keys[0]], keys[1:])


def get_recursive_dict_value(
    entity: dict,
    dot_separated_key: str,
    missing_key_handler: typing.Literal['skip', 'exception'],
):
    parts = dot_separated_key.split('.')
    if not parts:
        raise ValueError("dot_separated_key required")

    return recursive_dict_fetch(entity, parts, missing_key_handler=missing_key_handler)


def _dict_update_by_key_split(
    entity: dict,
    keys: list,
    new_value,
    missing_key_handler: Literal['skip', 'exception', 'add_missing'],
) -> dict | None:
    _first_key = keys[0]
    if _first_key not in entity:
        return None

    if entity[_first_key] is None:
        return None

    _current_entity_ref = entity
    for _key in keys[:-1]:
        if _current_entity_ref is None:
            return None

        if not isinstance(_current_entity_ref, dict):
            match missing_key_handler:
                case 'exception':
                    raise ValueError(f"Expected nested dictionaries, {_key} value is not a dict")
                case 'skip':
                    return entity
                case _:
                    raise Exception("Unhandled case for missing inner dict key")

        _current_entity_ref = _current_entity_ref[_key]

    if not isinstance(_current_entity_ref, (dict, list)):
        match missing_key_handler:
            case 'exception':
                raise ValueError(f"Expected nested dictionaries, {_current_entity_ref} is not a dict")
            case 'skip':
                return None
            case _:
                raise Exception("Unhandled case for missing inner dict key")

    final_key = keys[-1]
    _update_refs = []
    if isinstance(_current_entity_ref, list):
        _update_refs += _current_entity_ref
    elif isinstance(_current_entity_ref.get(final_key), list):
        _update_refs += _current_entity_ref[final_key]
    else:
        _update_refs.append(_current_entity_ref)

    for _ref in _update_refs:
        if isinstance(new_value, Callable):
            _new_value = new_value(_ref)
        elif isinstance(new_value, tuple):
            _new_value = new_value[0](_ref, **new_value[1])
        else:
            _new_value = new_value

        if final_key not in _ref:
            match missing_key_handler:
                case 'exception':
                    raise KeyError(f"Key {final_key} not found")
                case 'skip':
                    continue
                case 'add_missing':
                    _ref[final_key] = _new_value

        if _ref[final_key]:
            _ref[final_key] = _new_value

    return entity


def update_inner_dictionary_key(
    entity: dict,
    dot_separated_key: str,
    new_value: str | bool | int | dict | Tuple[Callable, dict] | Callable | None,
    missing_key_handler: Literal['skip', 'exception', 'add_missing'] = 'exception'
):
    """ Updates the inner dictionary key, and returns the first part of key path (root.branch.leaf returns `root[branch]`)"""
    parts = dot_separated_key.split('.')
    if not parts:
        raise ValueError("dot_separated_key required")

    updated_entity = _dict_update_by_key_split(entity, parts, new_value, missing_key_handler=missing_key_handler)
    if updated_entity is None:
        return None

    return updated_entity.get(parts[0])
