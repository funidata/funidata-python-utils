#  Copyright (c) 2025 Funidata Oy.
#  All rights reserved.
# ------------------------------------------------------------------------------

import logging
from enum import StrEnum
from typing import overload, Literal, TYPE_CHECKING

import httpx

from .protocols import SisImportable, SisPatchable, SisLegacyImportable, SisLegacyPatchable, SisDeletable
from ..auth.sis_auth import SisuConfig
from ..request_utils.async_httpx_requests import send_post_with_binary_err_search_httpx
from ..utils import batch


logger = logging.getLogger(__name__)
UNSET_BATCH_SIZE = -42


class DeleteMethodOverride(StrEnum):
    Import = "import"
    Patch = "patch"
    Delete = "delete"
    Automatic = "automatic"


@overload
async def soft_delete_from_sisu(
    sisu_config: SisuConfig,
    resource: SisDeletable,
    use_legacy_import: Literal[True, False],
    data: list[dict],
    batch_size: None,
    binary_search_max_depth: None,
    group_by_key: None,
    binary_err_search_sublists: Literal[False],
    max_parallel_requests: int,
    method_override: DeleteMethodOverride | None
) -> list[httpx.Response]:
    ...


@overload
async def soft_delete_from_sisu(
    sisu_config: SisuConfig,
    resource: SisImportable | SisPatchable,
    use_legacy_import: Literal[False],
    data: list[dict],
    batch_size: int | None,
    binary_search_max_depth: int | None,
    group_by_key: str | None,
    binary_err_search_sublists: bool,
    max_parallel_requests: int,
    method_override: DeleteMethodOverride | None
) -> list[httpx.Response]:
    ...


@overload
async def soft_delete_from_sisu(
    sisu_config: SisuConfig,
    resource: SisLegacyImportable | SisLegacyPatchable,
    use_legacy_import: Literal[True],
    data: list[dict],
    batch_size: int | None,
    binary_search_max_depth: int | None,
    group_by_key: str | None,
    binary_err_search_sublists: bool,
    max_parallel_requests: int,
    method_override: DeleteMethodOverride | None
) -> list[httpx.Response]:
    ...


async def soft_delete_from_sisu(
    sisu_config: SisuConfig,
    resource: SisImportable | SisLegacyImportable | SisPatchable | SisLegacyPatchable | SisDeletable,
    use_legacy_import: Literal[True, False],
    data: list[dict] | None = None,
    batch_size: int | None = UNSET_BATCH_SIZE,
    binary_search_max_depth: int | None = 0,
    group_by_key: str | None = None,
    binary_err_search_sublists: bool = False,
    max_parallel_requests: int = 1,
    method_override: DeleteMethodOverride | None = DeleteMethodOverride.Automatic,
) -> list[httpx.Response]:
    if not batch_size or batch_size == UNSET_BATCH_SIZE:
        if use_legacy_import:
            batch_size = resource.legacy_imports.default_import_limit
        else:
            batch_size = resource.imports.default_import_limit

    _batch_size = min(batch_size, 10000)
    # To make sure the document state is deleted for each deletable entity
    for _entity in data:
        _entity['documentState'] = 'DELETED'


    match method_override:
        case DeleteMethodOverride.Delete:
            return await _delete_with_delete_endpoint(
                batch_size=_batch_size,
                sisu_config=sisu_config,
                resource=resource,
                data=data
            )

        case DeleteMethodOverride.Patch:
            responses = await _delete_with_patch(
                data=data,
                resource=resource,
                sisu_config=sisu_config,
                batch_size=batch_size,
                binary_err_search_sublists=binary_err_search_sublists,
                binary_search_max_depth=binary_search_max_depth,
                group_by_key=group_by_key,
                max_parallel_requests=max_parallel_requests,
                use_legacy_import=True if use_legacy_import else False,
            )
            return responses

        case DeleteMethodOverride.Import:
            _path_postfix = resource.legacy_imports.endpoint if use_legacy_import else resource.imports.endpoint
            return await send_post_with_binary_err_search_httpx(
                path=f"{sisu_config.host}{_path_postfix}",
                payload=data,
                auth=sisu_config.get_integration_auth(),
                proxies=sisu_config.proxies,
                batch_size=_batch_size,
                binary_search_max_depth=binary_search_max_depth,
                binary_err_search_sublists=binary_err_search_sublists,
                group_by_key=group_by_key,
                method='POST',
                max_parallel_requests=max_parallel_requests,
            )

        case DeleteMethodOverride.Automatic | None:
            if isinstance(resource, SisDeletable):
                return await _delete_with_delete_endpoint(
                    batch_size=_batch_size,
                    sisu_config=sisu_config,
                    resource=resource,
                    data=data
                )

            if isinstance(resource, SisPatchable) or isinstance(resource, SisLegacyPatchable):
                responses = await _delete_with_patch(
                    data=data,
                    resource=resource,
                    sisu_config=sisu_config,
                    batch_size=batch_size,
                    binary_err_search_sublists=binary_err_search_sublists,
                    binary_search_max_depth=binary_search_max_depth,
                    group_by_key=group_by_key,
                    max_parallel_requests=max_parallel_requests,
                    use_legacy_import=True if use_legacy_import else False,
                )
                return responses

            _path_postfix = resource.legacy_imports.endpoint if use_legacy_import else resource.imports.endpoint
            responses = await send_post_with_binary_err_search_httpx(
                path=f"{sisu_config.host}{_path_postfix}",
                payload=data,
                auth=sisu_config.get_integration_auth(),
                proxies=sisu_config.proxies,
                batch_size=_batch_size,
                binary_search_max_depth=binary_search_max_depth,
                binary_err_search_sublists=binary_err_search_sublists,
                group_by_key=group_by_key,
                method='POST',
                max_parallel_requests=max_parallel_requests,
            )

            return responses


async def _delete_with_delete_endpoint(
    resource: SisDeletable,
    sisu_config: SisuConfig,
    batch_size: int | None,
    data: list[dict],
) -> list[httpx.Response]:
    _batches = batch(data, steps=batch_size)
    responses = []

    for _batch in _batches:
        _path_postfix = resource.delete.endpoint
        _delete_ids_list = list(set([x['id'] for x in _batch]))
        _delete_data = {
            'ids': _delete_ids_list,
        }

        proxy_mounts = None
        if sisu_config.proxies:
            proxy_mounts = {
                "http://": httpx.AsyncHTTPTransport(proxy=sisu_config.proxies.get('http')),
                "https://": httpx.AsyncHTTPTransport(proxy=sisu_config.proxies.get('https')),
            }

        client = httpx.AsyncClient(mounts=proxy_mounts, auth=sisu_config.get_integration_auth())

        _path = f"{sisu_config.host}{_path_postfix}"
        logger.debug("Sending POST with %d ids to %s", len(_delete_ids_list), _path)
        response = await client.post(
            _path,
            auth=sisu_config.get_integration_auth(),
            json=_delete_data,
            timeout=120,
        )
        responses.append(response)

    return responses


async def _delete_with_patch(
    data: list[dict] | None,
    sisu_config: SisuConfig,
    resource: SisLegacyPatchable | SisPatchable,
    use_legacy_import: Literal[True, False],
    group_by_key: str | None,
    batch_size: int | None,
    binary_err_search_sublists: bool,
    binary_search_max_depth: int | None,
    max_parallel_requests: int,
) -> list[httpx.Response]:
    # Maximum theoretical import payload size
    _batch_size = min(batch_size, 10000)

    _path_postfix = resource.legacy_patches.endpoint if use_legacy_import else resource.patches.endpoint
    responses = await send_post_with_binary_err_search_httpx(
        path=f"{sisu_config.host}{_path_postfix}",
        payload=data,
        auth=sisu_config.get_integration_auth(),
        proxies=sisu_config.proxies,
        batch_size=_batch_size,
        binary_search_max_depth=binary_search_max_depth,
        binary_err_search_sublists=binary_err_search_sublists,
        group_by_key=group_by_key,
        method='PATCH',
        max_parallel_requests=max_parallel_requests,
    )
    return responses


if TYPE_CHECKING:
    DeleteMethodOverride = Literal['import', 'patch', 'delete', 'automatic']
