#  Copyright (c) 2025 Funidata Oy.
#  All rights reserved.
# ------------------------------------------------------------------------------
import asyncio
from typing import Tuple, Any, Callable, Literal

import httpx
from httpx import Client

from . import async_httpx_requests


ACCEPTED_RESPONSE_CODES = {200, 201, 202, 204}


def batch(iterable, steps=1):
    length = len(iterable)
    for index in range(0, length, steps):
        yield iterable[index:min(index + steps, length)]


def _collect_suitable_batches_grouped_by_key(
    items_by_key: dict[Any, list[dict]],
    sorting_function: Callable = None,
    batch_size_trigger: int = 500,
) -> list[list[list[dict]]]:
    batches: list[list[list[dict]]] = []
    current_batch = []
    current_batch_size = 0

    sendable_lists_of_items = list(items_by_key.values())

    for index, values in enumerate(sendable_lists_of_items):
        current_batch.append(values)
        current_batch_size += len(values)
        if current_batch_size >= batch_size_trigger or index == len(sendable_lists_of_items) - 1:
            if sorting_function:
                current_batch = sorting_function(current_batch)

            batches.append(current_batch)
            current_batch = []
            current_batch_size = 0

    return batches


def send_get_httpx(
    path: str,
    auth: Tuple[str, str] | None = None,
    proxies: dict | None = None,
    params: dict | None = None,
) -> httpx.Response:
    client = _get_httpx_client(auth, proxies)
    with client:
        response = client.get(
            path,
            auth=auth,
            params=params,
            timeout=600,
        )
        return response


def _get_httpx_client(auth: tuple[str, str] | None, proxies: dict[Any, Any] | None) -> Client:
    proxy_mounts = {
        "http://": httpx.HTTPTransport(proxy=proxies.get('http')),
        "https://": httpx.HTTPTransport(proxy=proxies.get('https')),
    } if proxies else None
    client = httpx.Client(mounts=proxy_mounts, auth=auth)
    return client


def send_post_with_binary_err_search_httpx(
    path: str,
    payload: list[dict],
    group_by_key: str | None = None,
    auth: Tuple[str, str] | None = None,
    proxies: dict | None = None,
    params: dict | None = None,
    batch_size: int | None = None,
    binary_search_max_depth: int | None = None,
    binary_err_search_sublists: bool = True,
    method: Literal['POST', 'PATCH'] = 'POST',
    _state: dict[
                Literal['max_seen_depth', 'sent_requests'], int
            ] | None = None, ) -> list[httpx.Response]:
    return asyncio.run(
        async_httpx_requests.send_post_with_binary_err_search_httpx(
            path=path,
            payload=payload,
            group_by_key=group_by_key,
            auth=auth,
            proxies=proxies,
            params=params,
            batch_size=batch_size,
            binary_search_max_depth=binary_search_max_depth,
            binary_err_search_sublists=binary_err_search_sublists,
            method=method,
            _state=_state,
        )
    )
