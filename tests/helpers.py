import json
from collections import defaultdict

import httpx
import pytest


@pytest.fixture
def mock_client():
    return httpx.AsyncClient(
        transport=httpx.MockTransport(invalid_handler)
    )


def invalid_handler(request: httpx.Request):
    _content = json.loads(request.content)
    _failing_ids = [_x['id'] for _x in _content if _x.get('invalid')]
    _exception_ids = [_x['id'] for _x in _content if _x.get('exception')]
    if _exception_ids:
        return httpx.Response(
            status_code=500, json={"reason": "HV000029"}
        )
    if _failing_ids:
        return httpx.Response(
            status_code=422, json={"failingIds": _failing_ids}
        )
    return httpx.Response(200, json={"diu": "OK"})


def get_entity_counts_by_status_code(responses: list[httpx.Response]):
    counts_by_status_code = defaultdict(int)
    for response in responses:
        counts_by_status_code[response.status_code] += len(json.loads(response.request.content))

    return counts_by_status_code
