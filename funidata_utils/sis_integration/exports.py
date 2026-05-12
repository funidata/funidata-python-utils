#  Copyright (c) 2025 Funidata Oy.
#  All rights reserved.
# ------------------------------------------------------------------------------
import json
from typing import TextIO, overload, IO, Generator, Literal

from .protocols import SisExportable, SupportsExportAuthentication
from ..request_utils.httpx_requests import send_get_httpx


@overload
def _export_from_endpoint(
    sis_settings: SupportsExportAuthentication,
    endpoint: str,
    fp: None,
    since_ordinal: int = 0,
    export_limit: int = 1000,
    since: str = 'since'
) -> list[dict]:
    ...


@overload
def _export_from_endpoint(
    sis_settings: SupportsExportAuthentication,
    endpoint: str,
    fp: IO,
    since_ordinal: int = 0,
    export_limit: int = 1000,
    since: str = 'since'
) -> TextIO:
    ...


def _export_from_endpoint(
    sis_settings: SupportsExportAuthentication,
    endpoint: str,
    fp: IO | None,
    since_ordinal: int = 0,
    export_limit: int = 1000,
    since: str = 'since'
) -> IO | list[dict]:
    exported_entities = []
    for entities in export_from_endpoint_generator(
        sis_settings=sis_settings,
        endpoint=endpoint,
        since_ordinal=since_ordinal,
        export_limit=export_limit,
        since=since,
    ):
        if fp is None:
            exported_entities += entities
        else:
            for json_entity in entities:
                fp.write(json.dumps(json_entity))
                fp.write('\n')

        if len(entities) == 0 or len(entities) < export_limit:
            break

    if fp is None:
        return exported_entities

    return fp


def export_from_endpoint_generator(
    sis_settings: SupportsExportAuthentication,
    endpoint: str,
    since_ordinal: int = 0,
    export_limit: int = 1000,
    since: str = 'since'
) -> Generator[list[dict], None, None]:
    greatest_ordinal = since_ordinal
    export_limit = export_limit

    while True:
        sis_response = send_get_httpx(
            path=f"{sis_settings.host}{endpoint}",
            auth=sis_settings.get_export_auth(),
            params={since: greatest_ordinal, 'limit': export_limit},
            proxies=sis_settings.proxies,
        )
        if sis_response.status_code == 200:
            response_json = sis_response.json()
            entities: list[dict] = response_json.get("entities", [])

            yield entities

            if len(entities) == 0 or len(entities) < export_limit:
                break

            greatest_ordinal = response_json['greatestOrdinal']
        else:
            raise Exception(f"Error in export: {sis_response.status_code} : {sis_response.content}")


@overload
def export_from_sisu(
    sisu_config: SupportsExportAuthentication,
    resource: SisExportable,
    fp: None,
    since_ordinal: int,
    as_generator: Literal[False]
) -> list[dict]:
    ...


@overload
def export_from_sisu(
    sisu_config: SupportsExportAuthentication,
    resource: SisExportable,
    fp: IO,
    since_ordinal: int,
    as_generator: Literal[False]
) -> IO:
    ...


@overload
def export_from_sisu(
    sisu_config: SupportsExportAuthentication,
    resource: SisExportable,
    fp: None,
    since_ordinal: int,
    as_generator: Literal[True]
) -> Generator[list[dict], None, None]:
    ...


def export_from_sisu(
    sisu_config: SupportsExportAuthentication,
    resource: SisExportable,
    fp: IO | None = None,
    since_ordinal: int = 0,
    as_generator: bool = False
) -> list[dict] | IO | Generator[list[dict], None, None]:
    if as_generator:
        return export_from_endpoint_generator(
            endpoint=resource.exports.endpoint,
            export_limit=resource.exports.default_export_limit,
            sis_settings=sisu_config,
            since_ordinal=since_ordinal,
            since=resource.exports.since,
        )

    if fp:
        return _export_from_endpoint(
            endpoint=resource.exports.endpoint,
            export_limit=resource.exports.default_export_limit,
            sis_settings=sisu_config,
            since_ordinal=since_ordinal,
            since=resource.exports.since,
            fp=fp
        )

    return _export_from_endpoint(
        endpoint=resource.exports.endpoint,
        export_limit=resource.exports.default_export_limit,
        sis_settings=sisu_config,
        since_ordinal=since_ordinal,
        since=resource.exports.since,
        fp=None
    )
