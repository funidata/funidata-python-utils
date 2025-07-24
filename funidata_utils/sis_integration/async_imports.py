#  Copyright (c) 2025 Funidata Oy.
#  All rights reserved.
# ------------------------------------------------------------------------------

import logging
from typing import IO, overload, Literal

import httpx

from .protocols import SisImportable, SisPatchable, SisLegacyImportable, SisLegacyPatchable
from ..auth.sis_auth import SisuConfig
from ..request_utils.async_httpx_requests import send_post_with_binary_err_search_httpx


logger = logging.getLogger(__name__)
UNSET_BATCH_SIZE = -42


@overload
async def import_to_sisu(
    sisu_config: SisuConfig,
    resource: SisImportable,
    use_legacy_import: False,
    fp: IO,
    batch_size: int | None,
    binary_search_max_depth: int | None,
    group_by_key: str | None,
    binary_err_search_sublists: bool,
    max_parallel_requests: int,
) -> list[httpx.Response]:
    ...


@overload
async def import_to_sisu(
    sisu_config: SisuConfig,
    resource: SisLegacyImportable,
    use_legacy_import: True,
    fp: IO,
    batch_size: int | None,
    binary_search_max_depth: int | None,
    group_by_key: str | None,
    binary_err_search_sublists: bool,
    max_parallel_requests: int,
) -> list[httpx.Response]:
    ...


@overload
async def import_to_sisu(
    sisu_config: SisuConfig,
    resource: SisImportable,
    use_legacy_import: Literal[False],
    data: list[dict],
    batch_size: int | None,
    binary_search_max_depth: int | None,
    group_by_key: str | None,
    binary_err_search_sublists: bool,
    max_parallel_requests: int,
) -> list[httpx.Response]:
    ...


@overload
async def import_to_sisu(
    sisu_config: SisuConfig,
    resource: SisLegacyImportable,
    use_legacy_import: Literal[True],
    data: list[dict],
    batch_size: int | None,
    binary_search_max_depth: int | None,
    group_by_key: str | None,
    binary_err_search_sublists: bool,
    max_parallel_requests: int,
) -> list[httpx.Response]:
    ...


async def import_to_sisu(
    sisu_config: SisuConfig,
    resource: SisImportable | SisLegacyImportable,
    use_legacy_import: Literal[True, False],
    fp: IO | None = None,
    data: list[dict] | None = None,
    batch_size: int | None = UNSET_BATCH_SIZE,
    binary_search_max_depth: int | None = 0,
    group_by_key: str | None = None,
    binary_err_search_sublists: bool = False,
    max_parallel_requests: int = 1
) -> list[httpx.Response]:
    if fp:
        raise NotImplementedError("Not yet implemented")

    # Maximum theoretical import payload size
    if not batch_size or batch_size == UNSET_BATCH_SIZE:
        if use_legacy_import:
            batch_size = resource.legacy_imports.default_import_limit
        else:
            batch_size = resource.imports.default_import_limit

    _batch_size = min(batch_size, 10000)

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


async def patch_to_sisu(
    sisu_config: SisuConfig,
    resource: SisPatchable | SisLegacyPatchable,
    use_legacy_import: Literal[True, False],
    fp: IO | None = None,
    data: list[dict] | None = None,
    batch_size: int | None = UNSET_BATCH_SIZE,
    binary_search_max_depth: int | None = 0,
    group_by_key: str | None = None,
    binary_err_search_sublists: bool = False,
    max_parallel_requests: int = 1
) -> list[httpx.Response]:
    if fp:
        raise NotImplementedError("Not yet implemented")

    # Maximum theoretical import payload size
    if not batch_size or batch_size == UNSET_BATCH_SIZE:
        if use_legacy_import:
            batch_size = resource.legacy_patches.default_import_limit
        else:
            batch_size = resource.patches.default_import_limit

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
