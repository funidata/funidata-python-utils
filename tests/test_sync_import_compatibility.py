from typing import Literal

import pytest

from funidata_utils.request_utils import async_httpx_requests
from funidata_utils.request_utils.httpx_requests import send_post_with_binary_err_search_httpx
from tests.helpers import mock_client, get_entity_counts_by_status_code, _get_mock_async_httpx_client


def test_recursive_import_batching_with_sublists_off_no_fails(mock_client, monkeypatch):
    monkeypatch.setattr(async_httpx_requests, "_get_async_httpx_client", _get_mock_async_httpx_client)

    test_data = [
        {
            "id": 2,
            "person": 1,
        },
        {
            "id": 3,
            "person": 1
        },
        {
            "id": 3,
            "person": 2
        },
        {
            "id": 4,
            "person": 2
        },
        {
            "id": 4,
            "person": 3
        },
        {
            "id": 5,
            "person": 3
        }
    ]

    _state: dict[
        Literal['max_seen_depth', 'sent_requests'], int
    ] = {'max_seen_depth': 0, 'sent_requests': 0}
    results = send_post_with_binary_err_search_httpx(
        path="http://localhost",
        payload=test_data,
        binary_err_search_sublists=False,
        binary_search_max_depth=None,
        batch_size=10,
        _state=_state,
        group_by_key='person',
    )
    assert _state['max_seen_depth'] == 0
    assert _state['sent_requests'] == 1
    assert get_entity_counts_by_status_code(results)[200] == 6
    assert get_entity_counts_by_status_code(results).get(422) is None


def test_recursive_import_batching_with_sublists_off_one_fail(mock_client, monkeypatch):
    monkeypatch.setattr(async_httpx_requests, "_get_async_httpx_client", _get_mock_async_httpx_client)

    test_data = [
        {
            "id": 2,
            "person": 1,
            "invalid": True
        },
        {
            "id": 3,
            "person": 1
        },
        {
            "id": 3,
            "person": 2
        },
        {
            "id": 4,
            "person": 2
        },
        {
            "id": 4,
            "person": 3
        },
        {
            "id": 5,
            "person": 3
        }
    ]

    _state: dict[
        Literal['max_seen_depth', 'sent_requests'], int
    ] = {'max_seen_depth': 0, 'sent_requests': 0}
    results = send_post_with_binary_err_search_httpx(
        path="http://localhost",
        payload=test_data,
        binary_err_search_sublists=False,
        binary_search_max_depth=None,
        batch_size=10,
        group_by_key='person',
        _state=_state,
    )
    assert _state['max_seen_depth'] == 1
    assert _state['sent_requests'] == 3
    assert get_entity_counts_by_status_code(results)[200] == 4
    assert get_entity_counts_by_status_code(results)[422] == 2


def test_recursive_import_batching_with_sublists_off_multiple_fails(mock_client, monkeypatch):
    monkeypatch.setattr(async_httpx_requests, "_get_async_httpx_client", _get_mock_async_httpx_client)

    test_data = [
        {
            "id": 2,
            "person": 1,
            "invalid": True
        },
        {
            "id": 3,
            "person": 1,
            "invalid": True,
        },
        {
            "id": 3,
            "person": 2
        },
        {
            "id": 4,
            "person": 2
        },
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

    _state: dict[
        Literal['max_seen_depth', 'sent_requests'], int
    ] = {'max_seen_depth': 0, 'sent_requests': 0}
    results = send_post_with_binary_err_search_httpx(
        path="http://localhost",
        payload=test_data,
        binary_err_search_sublists=False,
        binary_search_max_depth=None,
        batch_size=10,
        group_by_key='person',
        _state=_state,
    )
    assert _state['max_seen_depth'] == 2
    assert _state['sent_requests'] == 5

    assert get_entity_counts_by_status_code(results)[200] == 2
    assert get_entity_counts_by_status_code(results)[422] == 4
