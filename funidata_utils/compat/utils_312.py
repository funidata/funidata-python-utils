from collections import defaultdict
from functools import reduce
from typing import Callable, Any


def group_by[T](
    seq: list[T],
    key: Callable
) -> dict[Any, list[T]]:
    return reduce(lambda grp, val: grp[key(val)].append(val) or grp, seq, defaultdict(list))
