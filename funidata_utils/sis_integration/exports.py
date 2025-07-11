from enum import Enum
from tempfile import NamedTemporaryFile
from typing import TextIO, overload, IO, Literal, Union

import simplejson
from pydantic import BaseModel

from ..auth.sis_credentials import SisuSettings
from ..request_utils.httpx_requests import send_get_httpx
from ..schemas.sisu import StudyRight


_EXPORT_LITERAL_RESOURCES = Literal[
    'organisations',
    'private-persons',
    'course-units',
    'educations',
    'modules',
    'attainments',
    'public-persons',
    'study-rights',
    'study-right-primalities',
    'study-year-templates',
]


@overload
def _export_from_endpoint(
    sis_settings: SisuSettings,
    endpoint: str,
    fp: None,
    since_ordinal: int = 0,
    export_limit: int = 1000,
) -> list[dict]:
    ...


@overload
def _export_from_endpoint(
    sis_settings: SisuSettings,
    endpoint: str,
    fp: IO,
    since_ordinal: int = 0,
    export_limit: int = 1000,
) -> TextIO:
    ...


def _export_from_endpoint(
    sis_settings: SisuSettings,
    endpoint: str,
    fp: IO | None,
    since_ordinal: int = 0,
    export_limit: int = 1000,
) -> IO | list[dict]:
    exported_entities = []
    greatest_ordinal = since_ordinal
    export_limit = export_limit

    while True:
        sis_response = send_get_httpx(
            path=f"{sis_settings.sis_host}{endpoint}",
            auth=sis_settings.get_export_auth(),
            params={'since': greatest_ordinal, 'limit': export_limit},
            proxies=sis_settings.socks_proxies,
        )
        if sis_response.status_code == 200:
            response_json = sis_response.json()
            entities = response_json.get("entities", [])

            if fp is None:
                exported_entities += entities
            else:
                for json_entity in entities:
                    fp.write(simplejson.dumps(json_entity))
                    fp.write('\n')

            if len(entities) == 0 or len(entities) < export_limit:
                break

            greatest_ordinal = response_json['greatestOrdinal']
        else:
            raise Exception(f"Error in export: {sis_response.status_code} : {sis_response.content}")

    if fp is None:
        return exported_entities

    return fp


@overload
def export_from_sisu(
    sisu_settings: SisuSettings,
    resource: _EXPORT_LITERAL_RESOURCES,
    fp: None = None,
    since_ordinal: int = 0,
) -> list[dict]:
    ...


@overload
def export_from_sisu(
    sisu_settings: SisuSettings,
    resource: _EXPORT_LITERAL_RESOURCES,
    fp: IO,
    since_ordinal: int = 0,
) -> IO:
    ...


def export_from_sisu(
    sisu_settings: SisuSettings,
    resource: _EXPORT_LITERAL_RESOURCES,
    fp: IO | None = None,
    since_ordinal: int = 0,
) -> list[dict] | IO:
    ori_resources = {
        'private-persons': {
            'endpoint': '/ori/api/persons/v1/export',
            'export_limit': 1500,
        },
        'attainments': {
            'endpoint': '/ori/api/attainments/v1/export',
            'export_limit': 2500,
        },
        'study-rights': {
            'endpoint': '/ori/api/study-rights/v1/export',
            'export_limit': 1000,
        },
        'study-right-primalities': {
            'endpoint': '/ori/api/study-right-primalities/v1/export',
            'export_limit': 1000,
        }
    }

    kori_resources = {
        'organisations': {
            'endpoint': '/kori/api/organisations/v2/export',
            'export_limit': 1500
        },
        'course-units': {
            'endpoint': '/kori/api/course-units/v1/export',
            'export_limit': 1500
        },
        'educations': {
            'endpoint': '/kori/api/educations/v1/export',
            'export_limit': 1000
        },
        'modules': {
            'endpoint': '/kori/api/modules/v1/export',
            'export_limit': 1000
        },
        'public-persons': {
            'endpoint': '/kori/api/persons/v1/export',
            'export_limit': 1500
        },
        'study-year-templates': {
            'endpoint': '/kori/api/study-year-templates/v1/export',
            'export_limit': 1000
        },
    }
    resource_maps = ori_resources | kori_resources

    if fp:
        return _export_from_endpoint(
            endpoint=resource_maps[resource]['endpoint'],
            export_limit=resource_maps[resource]['export_limit'],
            sis_settings=sisu_settings,
            since_ordinal=since_ordinal,
            fp=fp
        )

    return _export_from_endpoint(
        endpoint=resource_maps[resource]['endpoint'],
        export_limit=resource_maps[resource]['export_limit'],
        sis_settings=sisu_settings,
        since_ordinal=since_ordinal,
        fp=None
    )
