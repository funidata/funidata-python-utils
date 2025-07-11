import logging
from typing import IO, Literal, overload

import httpx

from ..auth.sis_credentials import SisuSettings
from ..request_utils.async_httpx_requests import send_post_with_binary_err_search_httpx


logger = logging.getLogger(__name__)
DEFAULT_BATCH_SIZE = 500

_EXPORT_LITERAL_RESOURCES = Literal[
    'organisations',
    'private-persons',
    'course-units',
    'educations',
    'modules',
    'access-role-person-assignment',
    'attainments',
    'studyrights',
    'term-registrations',
    'thesis',
    'mobility-periods',
]


@overload
async def import_to_sisu(
    sisu_settings: SisuSettings,
    resource: _EXPORT_LITERAL_RESOURCES,
    fp: IO,
    batch_size: int,
    binary_search_max_depth: int | None,
    group_by_key: str | None,
    binary_err_search_sublists: bool,
    max_parallel_requests: int,
) -> list[httpx.Response]:
    ...


@overload
async def import_to_sisu(
    sisu_settings: SisuSettings,
    resource: _EXPORT_LITERAL_RESOURCES,
    data: list[dict],
    batch_size: int,
    binary_search_max_depth: int | None,
    group_by_key: str | None,
    binary_err_search_sublists: bool,
    max_parallel_requests: int,
) -> list[httpx.Response]:
    ...


async def import_to_sisu(
    sisu_settings: SisuSettings,
    resource: _EXPORT_LITERAL_RESOURCES,
    fp: IO | None = None,
    data: list[dict] | None = None,
    batch_size: int = DEFAULT_BATCH_SIZE,
    binary_search_max_depth: int | None = 0,
    group_by_key: str | None = None,
    binary_err_search_sublists: bool = False,
    max_parallel_requests: int = 1
) -> list[httpx.Response]:
    ori_resources = {
        'private-persons': {
            'endpoint': '/ori/api/persons/v1/import',
        },
        'access-role-person-assignment': {
            'endpoint': '/ori/api/access-roles-person-assignments/v1/import',
        },
        'attainments': {
            'endpoint': '/ori/api/attainments/v1/import/legacy',
        },
        'studyrights': {
            'endpoint': '/ori/api/study-rights/v1/import',
        },
        'term-registrations': {
            'endpoint': '/ori/api/term-registrations/v1/import',
        },
        'thesis': {
            'endpoint': '/ori/api/thesis/v1/import',
        },
        'mobility-periods': {
            'endpoint': '/ori/api/mobility-periods/v1/import',
        },
    }

    kori_resources = {
        'organisations': {
            'endpoint': '/kori/api/organisations/v2/import',
        },
        'course-units': {
            'endpoint': '/kori/api/course-units/v1/import',
        },
        'educations': {
            'endpoint': '/kori/api/educations/v1/import',
        },
        'modules': {
            'endpoint': '/kori/api/modules/v1/import',
        },
    }
    resource_maps = ori_resources | kori_resources

    if fp:
        raise NotImplementedError("Not yet implemented")

    # Maximum theoretical import payload size
    _batch_size = min(batch_size, 10000)

    responses = await send_post_with_binary_err_search_httpx(
        path=f"{sisu_settings.sis_host}{resource_maps[resource]['endpoint']}",
        payload=data,
        auth=sisu_settings.get_integration_auth(),
        proxies=sisu_settings.socks_proxies,
        batch_size=_batch_size,
        binary_search_max_depth=binary_search_max_depth,
        binary_err_search_sublists=binary_err_search_sublists,
        group_by_key=group_by_key,
        method='POST',
        max_parallel_requests=max_parallel_requests,
    )

    return responses


async def patch_to_sisu(
    sisu_settings: SisuSettings,
    resource: Literal[
        'modules',
        'private-persons',
        'attainments',
    ],
    fp: IO | None = None,
    data: list[dict] | None = None,
    batch_size: int = DEFAULT_BATCH_SIZE,
    binary_search_max_depth: int | None = 0,
    group_by_key: str | None = None,
    binary_err_search_sublists: bool = False,
    max_parallel_requests: int = 1
) -> list[httpx.Response]:
    ori_resources = {
        'private-persons': {
            'endpoint': '/ori/api/persons/v1/import',
        },
        'attainments': {
            'endpoint': '/ori/api/attainments/v1/import/legacy',
        },
    }

    kori_resources = {
        'modules': {
            'endpoint': '/kori/api/modules/v1/import',
        },
    }
    resource_maps = ori_resources | kori_resources

    if fp:
        raise NotImplementedError("Not yet implemented")

    # Maximum theoretical import payload size
    _batch_size = min(batch_size, 10000)

    responses = await send_post_with_binary_err_search_httpx(
        path=f"{sisu_settings.sis_host}{resource_maps[resource]['endpoint']}",
        payload=data,
        auth=sisu_settings.get_integration_auth(),
        proxies=sisu_settings.socks_proxies,
        batch_size=_batch_size,
        binary_search_max_depth=binary_search_max_depth,
        binary_err_search_sublists=binary_err_search_sublists,
        group_by_key=group_by_key,
        method='PATCH',
        max_parallel_requests=max_parallel_requests,
    )

    return responses
