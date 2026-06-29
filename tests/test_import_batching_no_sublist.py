import pytest

from funidata_utils.request_utils.async_httpx_requests import _binary_search_enabled_post_httpx
from tests.helpers import mock_client, get_entity_counts_by_status_code


@pytest.mark.asyncio
async def test_recursive_import_batching_with_sublists_off_no_fails(mock_client):
    test_data = [
        [
            {
                "id": 2,
                "person": 1,
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

    _state = {'max_seen_depth': 0}
    results = await _binary_search_enabled_post_httpx(
        path="http://localhost",
        payload=test_data,
        client=mock_client,
        binary_err_search_sublists=False,
        binary_search_max_depth=None,
        _state=_state,
    )
    assert _state['max_seen_depth'] == 0
    assert _state['sent_requests'] == 1
    assert get_entity_counts_by_status_code(results)[200] == 6
    assert get_entity_counts_by_status_code(results).get(422) is None


@pytest.mark.asyncio
async def test_recursive_import_batching_with_sublists_off_one_fail(mock_client):
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

    _state = {'max_seen_depth': 0}
    results = await _binary_search_enabled_post_httpx(
        path="http://localhost",
        payload=test_data,
        client=mock_client,
        binary_err_search_sublists=False,
        binary_search_max_depth=None,
        _state=_state,
    )
    assert _state['max_seen_depth'] == 1
    assert _state['sent_requests'] == 3
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

    _state = {'max_seen_depth': 0}
    results = await _binary_search_enabled_post_httpx(
        path="http://localhost",
        payload=test_data,
        client=mock_client,
        binary_err_search_sublists=False,
        binary_search_max_depth=None,
        _state=_state,
    )
    assert _state['max_seen_depth'] == 2
    assert _state['sent_requests'] == 5

    assert get_entity_counts_by_status_code(results)[200] == 2
    assert get_entity_counts_by_status_code(results)[422] == 4


@pytest.mark.asyncio
async def test_recursive_import_batching_with_sublists_off_all_fails(mock_client):
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
                "person": 2,
                "invalid": True,
            },
            {
                "id": 4,
                "person": 2,
                "invalid": True,
            }
        ],
        [
            {
                "id": 4,
                "person": 3,
                "invalid": True,
            },
            {
                "id": 5,
                "person": 3,
                "invalid": True,
            }
        ]
    ]

    _state = {'max_seen_depth': 0}
    results = await _binary_search_enabled_post_httpx(
        path="http://localhost",
        payload=test_data,
        client=mock_client,
        binary_err_search_sublists=False,
        binary_search_max_depth=None,
        _state=_state,
    )
    assert _state['max_seen_depth'] == 0
    assert _state['sent_requests'] == 1

    assert get_entity_counts_by_status_code(results).get(200) is None
    assert get_entity_counts_by_status_code(results)[422] == 6


@pytest.mark.asyncio
async def test_recursive_import_batching_with_sublists_off_all_exceptions(mock_client):
    test_data = [
        [
            {
                "id": 2,
                "person": 1,
                "exception": True
            },
            {
                "id": 3,
                "person": 1,
                "exception": True,
            }
        ],
        [
            {
                "id": 3,
                "person": 2,
                "exception": True,
            },
            {
                "id": 4,
                "person": 2,
                "exception": True,
            }
        ],
        [
            {
                "id": 4,
                "person": 3,
                "exception": True,
            },
            {
                "id": 5,
                "person": 3,
                "exception": True,
            }
        ]
    ]

    _state = {'max_seen_depth': 0}
    results = await _binary_search_enabled_post_httpx(
        path="http://localhost",
        payload=test_data,
        client=mock_client,
        binary_err_search_sublists=False,
        binary_search_max_depth=None,
        _state=_state,
    )
    assert _state['max_seen_depth'] == 2
    assert _state['sent_requests'] == 5


    assert get_entity_counts_by_status_code(results).get(200) is None
    assert get_entity_counts_by_status_code(results)[500] == 6


@pytest.mark.asyncio
async def test_recursive_import_batching_with_sublists_off_all_exceptions_limited_max_depth(mock_client):
    test_data = [
        [
            {
                "id": 2,
                "person": 1,
                "exception": True
            },
            {
                "id": 3,
                "person": 1,
                "exception": True,
            }
        ],
        [
            {
                "id": 3,
                "person": 2,
                "exception": True,
            },
            {
                "id": 4,
                "person": 2,
                "exception": True,
            }
        ],
        [
            {
                "id": 4,
                "person": 3,
                "exception": True,
            },
            {
                "id": 5,
                "person": 3,
                "exception": True,
            }
        ]
    ]

    _state = {'max_seen_depth': 0}
    results = await _binary_search_enabled_post_httpx(
        path="http://localhost",
        payload=test_data,
        client=mock_client,
        binary_err_search_sublists=False,
        binary_search_max_depth=None,
        _state=_state,
    )
    assert _state['max_seen_depth'] == 2

    _state = {'max_seen_depth': 0}
    results = await _binary_search_enabled_post_httpx(
        path="http://localhost",
        payload=test_data,
        client=mock_client,
        binary_err_search_sublists=False,
        binary_search_max_depth=1,
        _state=_state,
    )
    assert _state['max_seen_depth'] == 1
    assert _state['sent_requests'] == 3


    assert get_entity_counts_by_status_code(results).get(200) is None
    assert get_entity_counts_by_status_code(results)[500] == 6