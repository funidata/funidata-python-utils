import json
from collections import defaultdict

import pytest

from funidata_utils.request_utils.async_httpx_requests import _binary_search_enabled_post_httpx

import httpx

from funidata_utils.utils import group_by


def invalid_handler(request: httpx.Request):
    _content = json.loads(request.content)
    _failing_ids = [_x['id'] for _x in _content if _x.get('invalid')]
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


@pytest.fixture
def mock_client():
    return httpx.AsyncClient(
        transport=httpx.MockTransport(invalid_handler)
    )


@pytest.mark.asyncio
async def test_recursive_import_batching_with_sublists_off(mock_client):
    test_data = [
        [
            {
                "id": 2,
                "person": 1,
                "invalid": True
            },
            {
                "id": 3,
                "person": 1
            }
        ],
        [
            {
                "id": 3,
                "person": 2
            },
            {
                "id": 4,
                "person": 2
            }
        ],
        [
            {
                "id": 4,
                "person": 3
            },
            {
                "id": 5,
                "person": 3
            }
        ]
    ]

    results = await _binary_search_enabled_post_httpx(
        path="http://localhost",
        payload=test_data,
        auth=None,
        client=mock_client,
        binary_search_depth=0,
        binary_err_search_sublists=False,
        binary_search_max_depth=None,
    )
    assert get_entity_counts_by_status_code(results)[200] == 4
    assert get_entity_counts_by_status_code(results)[422] == 2


@pytest.mark.asyncio
async def test_recursive_import_batching_with_sublists_off_multiple_fails(mock_client):
    test_data = [
        [
            {
                "id": 2,
                "person": 1,
                "invalid": True
            },
            {
                "id": 3,
                "person": 1,
                "invalid": True,
            }
        ],
        [
            {
                "id": 3,
                "person": 2
            },
            {
                "id": 4,
                "person": 2
            }
        ],
        [
            {
                "id": 4,
                "person": 3
            },
            {
                "id": 5,
                "person": 3,
                "invalid": True,
            }
        ]
    ]

    results = await _binary_search_enabled_post_httpx(
        path="http://localhost",
        payload=test_data,
        auth=None,
        client=mock_client,
        binary_search_depth=0,
        binary_err_search_sublists=False,
        binary_search_max_depth=None,
    )

    assert get_entity_counts_by_status_code(results)[200] == 4
    assert get_entity_counts_by_status_code(results)[422] == 2


@pytest.mark.asyncio
async def test_recursive_import_batching_with_sublists_on(mock_client):
    test_data = [
        [
            {
                "id": 2,
                "person": 1,
                "invalid": True
            },
            {
                "id": 3,
                "person": 1
            }
        ],
        [
            {
                "id": 3,
                "person": 2
            },
            {
                "id": 4,
                "person": 2
            }
        ],
        [
            {
                "id": 4,
                "person": 3
            },
            {
                "id": 5,
                "person": 3
            }
        ]
    ]

    results = await _binary_search_enabled_post_httpx(
        path="http://localhost",
        payload=test_data,
        auth=None,
        client=mock_client,
        binary_err_search_sublists=True,
        binary_search_depth=0,
        binary_search_max_depth=None
    )
    assert get_entity_counts_by_status_code(results)[200] == 5
    assert get_entity_counts_by_status_code(results)[422] == 1
