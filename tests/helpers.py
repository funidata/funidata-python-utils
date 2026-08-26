import json
from collections import defaultdict

import httpx
import pytest

from funidata_utils.request_utils import httpx_requests


def _get_mock_async_httpx_client(*args, **kwargs):
    return httpx.AsyncClient(
        transport=httpx.MockTransport(mock_http_handler)
    )


def _get_mock_httpx_client(*args, **kwargs):
    return httpx.Client(
        transport=httpx.MockTransport(mock_http_handler)
    )


@pytest.fixture
def mock_client(monkeypatch):
    return _get_mock_async_httpx_client()


@pytest.fixture
def mock_sync_client(monkeypatch):
    return _get_mock_httpx_client()


def mock_http_handler(request: httpx.Request):
    match request.method:
        case 'POST':
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
        case 'GET':
            return httpx.Response(
                200,
                json=dict(
                    entities=[
                        {"id": "12345", "fish": 1, "diu": 2, "documentState": "ACTIVE", "firstNames": "John", "lastName": "Deere"},
                        {"id": "12346", "documentState": "DRAFT", "firstNames": "John", "lastName": "Deere"},
                        {"id": "12347", "kuha": 1, "fish": 2, "documentState": "DELETED", "firstNames": "John", "lastName": "Deere"},
                    ]
                )
            )


def get_entity_counts_by_status_code(responses: list[httpx.Response]):
    counts_by_status_code = defaultdict(int)
    for response in responses:
        counts_by_status_code[response.status_code] += len(json.loads(response.request.content))

    return counts_by_status_code
