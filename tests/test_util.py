import pytest
from funidata_utils.utils import group_by


def test_group_by():
    data = [dict(id=1, type=1), dict(id=2, type=1), dict(id=3, type=2)]

    grouping = group_by(data, lambda x: x['type'] == 1)

    assert grouping[1] == [dict(id=1, type=1), dict(id=2, type=1)]
