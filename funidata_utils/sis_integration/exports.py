#  Copyright (c) 2025 Funidata Oy.
#  All rights reserved.
# ------------------------------------------------------------------------------
import json
import logging
from collections import defaultdict
from typing import TextIO, overload, IO, Generator, Literal

from .protocols import SisExportable, SupportsExportAuthentication, ScramblingClass, SisExportableSupportScrambling
from ..data_scramblers.generic_sis_scramble import SisMetadataScrambler, UnprocessedKeysDropperScrambler
from ..request_utils.httpx_requests import send_get_httpx


logger = logging.getLogger(__name__)


@overload
def _export_from_endpoint(
    sis_settings: SupportsExportAuthentication,
    endpoint: str,
    fp: None,
    since_ordinal: int = 0,
    export_limit: int = 1000,
    since: str = 'since',
    params: dict | None = None,
    scrambling_classes: list[ScramblingClass] | None = None
) -> list[dict]:
    ...


@overload
def _export_from_endpoint(
    sis_settings: SupportsExportAuthentication,
    endpoint: str,
    fp: IO,
    since_ordinal: int = 0,
    export_limit: int = 1000,
    since: str = 'since',
    params: dict | None = None,
    scrambling_classes: list[ScramblingClass] | None = None
) -> TextIO:
    ...


def _export_from_endpoint(
    sis_settings: SupportsExportAuthentication,
    endpoint: str,
    fp: IO | None,
    since_ordinal: int = 0,
    export_limit: int = 1000,
    since: str = 'since',
    params: dict | None = None,
    scrambling_classes: list[ScramblingClass] | None = None
) -> IO | list[dict]:
    if not params:
        params = {}

    exported_entities = []
    for entities in export_from_endpoint_generator(
        sis_settings=sis_settings,
        endpoint=endpoint,
        since_ordinal=since_ordinal,
        export_limit=export_limit,
        since=since,
        params=params,
        scrambling_classes=scrambling_classes
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
    since: str = 'since',
    params: dict | None = None,
    scrambling_classes: list[ScramblingClass] | None = None
) -> Generator[list[dict], None, None]:
    greatest_ordinal = since_ordinal
    export_limit = export_limit
    if not params:
        params = {}

    scrambling_warning_triggered_keys = set()
    while True:
        sis_response = send_get_httpx(
            path=f"{sis_settings.host}{endpoint}",
            auth=sis_settings.get_export_auth(),
            params=params | {since: greatest_ordinal, 'limit': export_limit},
            proxies=sis_settings.proxies,
        )
        if sis_response.status_code == 200:
            response_json = sis_response.json()
            entities: list[dict] = response_json.get("entities", [])
            if scrambling_classes:
                scrambling_classes.append(SisMetadataScrambler)
                scrambling_classes.append(UnprocessedKeysDropperScrambler(scrambling_warning_triggered_keys))
                processed_keys = defaultdict(list)
                _data = [
                    scrambling_class.scramble(entity, processed_keys)
                    for entity in entities
                    for scrambling_class in scrambling_classes
                ]
                yield _data
            else:
                yield entities

            if len(entities) == 0 or len(entities) < export_limit:
                break

            greatest_ordinal = response_json['greatestOrdinal']
        else:
            raise Exception(f"Error in export: {sis_response.status_code} : {sis_response.content}")

    if scrambling_warning_triggered_keys:
        logger.warning("Original export data contains keys not handled in scrambling: %s", ', '.join(scrambling_warning_triggered_keys))


@overload
def export_from_sisu(
    sisu_config: SupportsExportAuthentication,
    resource: SisExportable,
    *,
    since_ordinal: int = 0,
    params: dict | None = None,
    fp: None = None,
    as_generator: Literal[False] = False,
    scramble: Literal[False] = False,
) -> list[dict]:
    ...


@overload
def export_from_sisu(
    sisu_config: SupportsExportAuthentication,
    resource: SisExportableSupportScrambling,
    *,
    since_ordinal: int = 0,
    params: dict | None = None,
    fp: None = None,
    as_generator: Literal[False] = False,
    scramble: bool = False,
) -> list[dict]:
    ...


@overload
def export_from_sisu(
    sisu_config: SupportsExportAuthentication,
    resource: SisExportable,
    *,
    since_ordinal: int = 0,
    params: dict | None = None,
    fp: None = None,
    as_generator: Literal[True] = True,
    scramble: Literal[False] = False,
) -> Generator[list[dict], None, None]:
    ...


@overload
def export_from_sisu(
    sisu_config: SupportsExportAuthentication,
    resource: SisExportableSupportScrambling,
    *,
    since_ordinal: int = 0,
    params: dict | None = None,
    fp: None = None,
    as_generator: Literal[True] = True,
    scramble: bool = True,
) -> Generator[list[dict], None, None]:
    ...


@overload
def export_from_sisu(
    sisu_config: SupportsExportAuthentication,
    resource: SisExportable,
    *,
    since_ordinal: int = 0,
    params: dict | None = None,
    fp: IO,
    as_generator: Literal[False] = False,
    scramble: Literal[False] = False,
) -> IO:
    ...


@overload
def export_from_sisu(
    sisu_config: SupportsExportAuthentication,
    resource: SisExportableSupportScrambling,
    *,
    since_ordinal: int = 0,
    params: dict | None = None,
    fp: IO,
    as_generator: Literal[False] = False,
    scramble: bool = True,
) -> IO:
    ...


def export_from_sisu(
    sisu_config: SupportsExportAuthentication,
    resource: SisExportable | SisExportableSupportScrambling,
    since_ordinal: int = 0,
    params: dict | None = None,
    fp: IO | None = None,
    as_generator: bool = False,
    scramble: bool = False,
) -> list[dict] | IO | Generator[list[dict], None, None]:
    if scramble:
        scrambling_classes = resource.scrambling_classes
        if not scrambling_classes:
            raise Exception("Requested scrambling for a resource that has no scrambling_classes")
    else:
        scrambling_classes = None

    if as_generator:
        return export_from_endpoint_generator(
            endpoint=resource.exports.endpoint,
            export_limit=resource.exports.default_export_limit,
            sis_settings=sisu_config,
            since_ordinal=since_ordinal,
            since=resource.exports.since,
            params=params,
            scrambling_classes=scrambling_classes,
        )

    if fp:
        return _export_from_endpoint(
            endpoint=resource.exports.endpoint,
            export_limit=resource.exports.default_export_limit,
            sis_settings=sisu_config,
            since_ordinal=since_ordinal,
            since=resource.exports.since,
            fp=fp,
            params=params,
            scrambling_classes=scrambling_classes,
        )

    return _export_from_endpoint(
        endpoint=resource.exports.endpoint,
        export_limit=resource.exports.default_export_limit,
        sis_settings=sisu_config,
        since_ordinal=since_ordinal,
        since=resource.exports.since,
        fp=None,
        params=params,
        scrambling_classes=scrambling_classes,
    )
