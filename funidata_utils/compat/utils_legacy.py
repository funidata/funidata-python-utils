from collections import defaultdict
from functools import reduce
from typing import Callable, Any, TypeVar


T = TypeVar('T')


def group_by(
    seq: list[T],
    key: Callable
) -> dict[Any, list[T]]:
    return reduce(lambda grp, val: grp[key(val)].append(val) or grp, seq, defaultdict(list))
