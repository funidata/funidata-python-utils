#  Copyright (c) 2025 Funidata Oy.
#  All rights reserved.
# ------------------------------------------------------------------------------

from typing import Tuple, Any, Callable, Literal

import httpx
from ..utils import flatten, group_by


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
    proxy_mounts = {
        "http://": httpx.HTTPTransport(proxy=proxies.get('http')),
        "https://": httpx.HTTPTransport(proxy=proxies.get('https')),
    }
    client = httpx.Client(mounts=proxy_mounts, auth=auth)
    response = client.get(
        path,
        auth=auth,
        params=params,
        timeout=600,
    )
    return response


def _binary_search_enabled_post_httpx(
    path: str,
    payload: list[dict] | list[list[dict]],
    client: httpx.Client,
    auth: Tuple[str, str] | None = None,
    params: dict | None = None,
    binary_search_depth: int = 0,
    binary_search_max_depth: int | None = None,
    binary_err_search_sublists: bool = True,
    method: Literal['POST', 'PATCH'] = 'POST',
) -> list[httpx.Response]:
    is_complex_list_of_batches = False
    if isinstance(payload, list) and all(isinstance(x, list) for x in payload[::3]):
        is_complex_list_of_batches = True

    match method:
        case 'POST':
            response = client.post(
                path,
                auth=auth,
                json=flatten(payload) if is_complex_list_of_batches else payload,
                params=params,
                timeout=60,
            )

        case 'PATCH':
            response = client.patch(
                path,
                auth=auth,
                json=flatten(payload) if is_complex_list_of_batches else payload,
                params=params,
                timeout=60,
            )

        case _:
            raise Exception(f'Unsupported method: {method}')

    if (
        binary_search_max_depth == 0 or
        (binary_search_max_depth and binary_search_depth >= binary_search_max_depth)
        or response.status_code in ACCEPTED_RESPONSE_CODES
    ):
        return [response]

    if not is_complex_list_of_batches:
        if len(payload) <= 1:
            return [response]
    else:
        if len(payload) <= 1 and not binary_err_search_sublists:
            return [response]

        if len(payload) == 1 and binary_err_search_sublists:
            return _binary_search_enabled_post_httpx(
                path=path,
                payload=flatten(payload),
                auth=auth,
                params=params,
                client=client,
                binary_search_depth=binary_search_depth + 1,
                binary_search_max_depth=binary_search_max_depth,
                binary_err_search_sublists=False,
                method=method,
            )

    first_half_responses = _binary_search_enabled_post_httpx(
        path=path,
        payload=payload[::2],
        auth=auth,
        params=params,
        client=client,
        binary_search_depth=binary_search_depth + 1,
        binary_search_max_depth=binary_search_max_depth,
        binary_err_search_sublists=binary_err_search_sublists,
        method=method,
    )
    second_half_responses = _binary_search_enabled_post_httpx(
        path=path,
        payload=payload[1::2],
        auth=auth,
        params=params,
        client=client,
        binary_search_depth=binary_search_depth + 1,
        binary_search_max_depth=binary_search_max_depth,
        binary_err_search_sublists=binary_err_search_sublists,
        method=method,
    )
    return first_half_responses + second_half_responses


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
) -> list[httpx.Response]:
    if len(payload) <= 0:
        raise Exception(f"Payload missing when attempting to POST to : {path}")

    proxy_mounts = None
    if proxies:
        proxy_mounts = {
            "http://": httpx.HTTPTransport(proxy=proxies.get('http')),
            "https://": httpx.HTTPTransport(proxy=proxies.get('https')),
        }

    client = httpx.Client(mounts=proxy_mounts, auth=auth)

    if group_by_key:
        items_by_key = group_by(payload, lambda x: x[group_by_key])
        batches = _collect_suitable_batches_grouped_by_key(
            items_by_key=items_by_key,
            sorting_function=None,
            batch_size_trigger=batch_size,
        )
        """
        Creates a structure that contains the grouped data as lists of the original groups 
        that then reside in lists approximately of the size batch_size
        Could be useful for example for grouping attainments of persons, so that the original context
        of which attainments belong to which person can be separately sent in one batch.
        [
            [ [1], [2,3] ],
            [ [4,5,6] ],
            [ [7,8], [10,11,12,13,14] ],
        ]
        """
        responses = []

        for _batch in batches:
            batch_responses = _binary_search_enabled_post_httpx(
                path=path,
                payload=_batch,
                params=params,
                auth=auth,
                client=client,
                binary_search_depth=0,
                binary_search_max_depth=binary_search_max_depth,
                binary_err_search_sublists=binary_err_search_sublists,
                method=method,
            )
            responses += batch_responses
        return responses

    # Is not group_by'ed -> If batch size is not configured, try sending everything
    if not batch_size:
        return _binary_search_enabled_post_httpx(
            path=path,
            payload=payload,
            params=params,
            auth=auth,
            client=client,
            binary_search_depth=0,
            binary_search_max_depth=binary_search_max_depth,
            binary_err_search_sublists=binary_err_search_sublists,
            method=method,
        )

    # When batch size is configured, batch the payload
    responses = []
    for batched_payload in batch(payload, batch_size):
        batch_responses = _binary_search_enabled_post_httpx(
            path=path,
            payload=batched_payload,
            params=params,
            auth=auth,
            client=client,
            binary_search_depth=0,
            binary_search_max_depth=binary_search_max_depth,
            binary_err_search_sublists=binary_err_search_sublists,
            method=method,
        )
        responses += batch_responses

    return responses
