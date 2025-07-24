#  Copyright (c) 2025 Funidata Oy.
#  All rights reserved.
# ------------------------------------------------------------------------------

from collections import defaultdict
from functools import reduce
from statistics import mean, stdev
from typing import Any, Generator, Callable

import httpx


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


def group_by[T](
    seq: list[T],
    key: Callable
) -> dict[Any, list[T]]:
    return reduce(lambda grp, val: grp[key(val)].append(val) or grp, seq, defaultdict(list))


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
