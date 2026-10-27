#  Copyright (c) 2025 Funidata Oy.
#  All rights reserved.
# ------------------------------------------------------------------------------
import json
import logging
from dataclasses import dataclass, field
from typing import TextIO, overload, IO, Generator, Literal

from .protocols import SisExportable, SupportsExportAuthentication, ScramblingClass, SisExportableSupportScrambling
from ..data_scramblers.generic_sis_scramble import SisMetadataScrambler, UnprocessedKeysDropperScrambler
from ..request_utils.httpx_requests import send_get_httpx


logger = logging.getLogger(__name__)


@dataclass
class ExportPage:
    """One page of a SISU export, as returned by a single request to the export endpoint."""
    entities: list[dict] = field(default_factory=list)
    greatest_ordinal: int = 0
    """Ordinal to pass as `since` to continue the export after this page."""
    has_more: bool = False
    """Whether SISU reported more entities after this page."""


def _resolve_scrambling_classes(
    resource: SisExportable | SisExportableSupportScrambling,
    scramble: bool,
) -> list[ScramblingClass] | None:
    if not scramble:
        return None

    scrambling_classes = resource.scrambling_classes
    if not scrambling_classes:
        raise Exception("Requested scrambling for a resource that has no scrambling_classes")

    return scrambling_classes


def _export_pages_from_endpoint(
    sis_settings: SupportsExportAuthentication,
    endpoint: str,
    since_ordinal: int = 0,
    export_limit: int = 1000,
    since: str = 'since',
    params: dict | None = None,
    scrambling_classes: list[ScramblingClass] | None = None
) -> Generator[ExportPage, None, None]:
    greatest_ordinal = since_ordinal
    if not params:
        params = {}

    scrambling_warning_triggered_keys: set[str] = set()
    reported_keys: set[str] = set()
    _scrambling_classes = None
    if scrambling_classes:
        _scrambling_classes = [
            *scrambling_classes,
            SisMetadataScrambler,
            UnprocessedKeysDropperScrambler(scrambling_warning_triggered_keys)
        ]

    while True:
        sis_response = send_get_httpx(
            path=f"{sis_settings.host}{endpoint}",
            auth=sis_settings.get_export_auth(),
            params=params | {since: greatest_ordinal, 'limit': export_limit},
            proxies=sis_settings.proxies,
        )
        if sis_response.status_code != 200:
            raise Exception(f"Error in export: {sis_response.status_code} : {sis_response.content}")

        response_json = sis_response.json()
        entities: list[dict] = response_json.get("entities", [])
        if _scrambling_classes:
            scrambled_entities = []
            for entity in entities:
                processed_keys = set()
                for scrambling_class in _scrambling_classes:
                    entity = scrambling_class.scramble(entity, processed_keys)
                scrambled_entities.append(entity)
            entities = scrambled_entities

            new_keys = scrambling_warning_triggered_keys - reported_keys
            if new_keys:
                logger.warning(
                    "Export data contains keys not handled in scrambling, thus they have been removed: %s",
                    ', '.join(sorted(new_keys))
                )
                reported_keys |= new_keys

        # An empty page can never continue, regardless of what SISU says; otherwise trust `hasMore`
        # and fall back to the page size when the endpoint does not report it.
        has_more = bool(entities) and bool(response_json.get("hasMore", len(entities) >= export_limit))
        greatest_ordinal = response_json.get("greatestOrdinal", greatest_ordinal)

        yield ExportPage(entities=entities, greatest_ordinal=greatest_ordinal, has_more=has_more)

        if not has_more:
            break

    if scrambling_warning_triggered_keys:
        logger.warning(
            "Original export data contains keys not handled in scrambling, thus have been removed: %s",
            ', '.join(sorted(scrambling_warning_triggered_keys))
        )


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
    for page in _export_pages_from_endpoint(
        sis_settings=sis_settings,
        endpoint=endpoint,
        since_ordinal=since_ordinal,
        export_limit=export_limit,
        since=since,
        params=params,
        scrambling_classes=scrambling_classes,
    ):
        yield page.entities


def export_pages_from_sisu(
    sisu_config: SupportsExportAuthentication,
    resource: SisExportable | SisExportableSupportScrambling,
    *,
    since_ordinal: int = 0,
    params: dict | None = None,
    scramble: bool = False,
    export_limit: int | None = None,
) -> Generator[ExportPage, None, None]:
    """
    Export a resource page by page, exposing SISU's `greatestOrdinal` and `hasMore` for every page.

    Use this when the caller needs to track where the export is (e.g. to resume later or to store
    data by ordinal). `export_limit` overrides the resource's default page size.
    """
    return _export_pages_from_endpoint(
        endpoint=resource.exports.endpoint,
        export_limit=export_limit or resource.exports.default_export_limit,
        sis_settings=sisu_config,
        since_ordinal=since_ordinal,
        since=resource.exports.since,
        params=params,
        scrambling_classes=_resolve_scrambling_classes(resource, scramble),
    )


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
    scrambling_classes = _resolve_scrambling_classes(resource, scramble)

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
