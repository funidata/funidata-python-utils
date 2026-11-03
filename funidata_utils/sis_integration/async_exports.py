#  Copyright (c) 2025 Funidata Oy.
#  All rights reserved.
# ------------------------------------------------------------------------------
"""
Async SISU exports. The sync functions in `exports.py` are thin wrappers around these.
"""
import json
import logging
from dataclasses import dataclass, field
from typing import overload, IO, Literal, AsyncGenerator

from .protocols import SisExportable, SupportsExportAuthentication, ScramblingClass, SisExportableSupportScrambling
from ..data_scramblers.generic_sis_scramble import SisMetadataScrambler, UnprocessedKeysDropperScrambler
from ..request_utils.async_httpx_requests import send_get_httpx


logger = logging.getLogger(__name__)


@dataclass
class ExportPage:
    """One page of a SISU export, as returned by a single request to the export endpoint."""
    entities: list[dict] = field(default_factory=list)
    greatest_ordinal: int = 0
    """Ordinal to pass as `since` to continue the export after this page."""
    has_more: bool = False
    """Whether SISU reported more entities after this page."""


async def export_pages_from_endpoint(
    sis_settings: SupportsExportAuthentication,
    endpoint: str,
    since_ordinal: int = 0,
    export_limit: int = 1000,
    since: str = 'since',
    params: dict | None = None,
    scrambling_classes: list[ScramblingClass] | None = None
) -> AsyncGenerator[ExportPage, None]:
    """
    Low-level variant of `export_pages_from_sisu` for callers that do not have a `SisExportable`
    resource: export an endpoint page by page, yielding `ExportPage` objects.
    """
    greatest_ordinal = since_ordinal
    if not params:
        params = {}

    scrambling_warning_triggered_keys: set[str] = set()
    reported_keys: set[str] = set()
    if scrambling_classes:
        scrambling_classes = [
            *scrambling_classes,
            SisMetadataScrambler,
            UnprocessedKeysDropperScrambler(scrambling_warning_triggered_keys)
        ]

    while True:
        sis_response = await send_get_httpx(
            path=f"{sis_settings.host}{endpoint}",
            auth=sis_settings.get_export_auth(),
            params=params | {since: greatest_ordinal, 'limit': export_limit},
            proxies=sis_settings.proxies,
        )
        if sis_response.status_code != 200:
            raise Exception(f"Error in export: {sis_response.status_code} : {sis_response.content}")

        response_json = sis_response.json()
        entities: list[dict] = response_json.get("entities", [])
        if scrambling_classes:
            scrambled_entities = []
            for entity in entities:
                processed_keys = set()
                for scrambling_class in scrambling_classes:
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

        # Trust SISU's `hasMore` when it is reported, even on an empty page (server-side filtering
        # can empty a window that still has data after it). Without `hasMore`, fall back to the
        # page size, which means an empty page ends the export.
        if "hasMore" in response_json:
            has_more = bool(response_json["hasMore"])
        else:
            has_more = len(entities) >= export_limit
        next_ordinal = response_json.get("greatestOrdinal")
        if has_more and (next_ordinal is None or next_ordinal <= greatest_ordinal):
            # Continuing would re-request the same page forever, so fail instead of looping.
            raise Exception(
                f"Error in export of {endpoint}: SISU reported more data after since={greatest_ordinal} "
                f"but greatestOrdinal did not advance (got {next_ordinal!r})"
            )
        if next_ordinal is not None:
            greatest_ordinal = next_ordinal

        yield ExportPage(entities=entities, greatest_ordinal=greatest_ordinal, has_more=has_more)

        if not has_more:
            break

    if scrambling_warning_triggered_keys:
        logger.warning(
            "Original export data contains keys not handled in scrambling, thus have been removed: %s",
            ', '.join(sorted(scrambling_warning_triggered_keys))
        )


async def export_from_endpoint_generator(
    sis_settings: SupportsExportAuthentication,
    endpoint: str,
    since_ordinal: int = 0,
    export_limit: int = 1000,
    since: str = 'since',
    params: dict | None = None,
    scrambling_classes: list[ScramblingClass] | None = None
) -> AsyncGenerator[list[dict], None]:
    """Like `export_pages_from_endpoint`, but yields only the entities of each page."""
    async for page in export_pages_from_endpoint(
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
) -> AsyncGenerator[ExportPage, None]:
    """
    Export a resource page by page, exposing SISU's `greatestOrdinal` and `hasMore` for every page.

    Returns an async generator (no `await` needed): `async for page in export_pages_from_sisu(...)`.
    Use this when the caller needs to track where the export is (e.g. to resume later or to store
    data by ordinal). `export_limit` overrides the resource's default page size.
    """
    scrambling_classes = None
    if scramble:
        scrambling_classes = resource.scrambling_classes
        if not scrambling_classes:
            raise Exception("Requested scrambling for a resource that has no scrambling_classes")

    return export_pages_from_endpoint(
        sis_settings=sisu_config,
        endpoint=resource.exports.endpoint,
        since_ordinal=since_ordinal,
        export_limit=export_limit or resource.exports.default_export_limit,
        since=resource.exports.since,
        params=params,
        scrambling_classes=scrambling_classes,
    )


@overload
async def export_from_sisu(
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
async def export_from_sisu(
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
async def export_from_sisu(
    sisu_config: SupportsExportAuthentication,
    resource: SisExportable,
    *,
    since_ordinal: int = 0,
    params: dict | None = None,
    fp: None = None,
    as_generator: Literal[True] = True,
    scramble: Literal[False] = False,
) -> AsyncGenerator[list[dict], None]:
    ...


@overload
async def export_from_sisu(
    sisu_config: SupportsExportAuthentication,
    resource: SisExportableSupportScrambling,
    *,
    since_ordinal: int = 0,
    params: dict | None = None,
    fp: None = None,
    as_generator: Literal[True] = True,
    scramble: bool = True,
) -> AsyncGenerator[list[dict], None]:
    ...


@overload
async def export_from_sisu(
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
async def export_from_sisu(
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


async def export_from_sisu(
    sisu_config: SupportsExportAuthentication,
    resource: SisExportable | SisExportableSupportScrambling,
    since_ordinal: int = 0,
    params: dict | None = None,
    fp: IO | None = None,
    as_generator: bool = False,
    scramble: bool = False,
) -> list[dict] | IO | AsyncGenerator[list[dict], None]:
    """
    Export a resource from SISU.

    With `as_generator=True` the awaited result is an async generator of entity pages:
    `gen = await export_from_sisu(..., as_generator=True)` then `async for entities in gen`.
    """
    pages = export_pages_from_sisu(
        sisu_config,
        resource,
        since_ordinal=since_ordinal,
        params=params,
        scramble=scramble,
    )

    if as_generator:
        return (page.entities async for page in pages)

    exported_entities: list[dict] = []
    async for page in pages:
        if fp is None:
            exported_entities += page.entities
        else:
            for json_entity in page.entities:
                fp.write(json.dumps(json_entity))
                fp.write('\n')

    if fp is None:
        return exported_entities

    return fp
