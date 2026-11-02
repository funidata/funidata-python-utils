#  Copyright (c) 2025 Funidata Oy.
#  All rights reserved.
# ------------------------------------------------------------------------------
"""
Synchronous SISU exports. These are thin wrappers that run the async implementations in
`async_exports.py` on a private event loop, so they cannot be called from inside a running
event loop (use `async_exports` directly there).
"""
import asyncio
import logging
from typing import TextIO, overload, IO, Generator, Literal

from . import async_exports
from .async_exports import ExportPage, _resolve_scrambling_classes  # noqa: F401 (re-exported)
from .protocols import SisExportable, SupportsExportAuthentication, ScramblingClass, SisExportableSupportScrambling
from ..utils import iterate_async_generator


logger = logging.getLogger(__name__)


def _export_pages_from_endpoint(
    sis_settings: SupportsExportAuthentication,
    endpoint: str,
    since_ordinal: int = 0,
    export_limit: int = 1000,
    since: str = 'since',
    params: dict | None = None,
    scrambling_classes: list[ScramblingClass] | None = None
) -> Generator[ExportPage, None, None]:
    return iterate_async_generator(async_exports._export_pages_from_endpoint(
        sis_settings=sis_settings,
        endpoint=endpoint,
        since_ordinal=since_ordinal,
        export_limit=export_limit,
        since=since,
        params=params,
        scrambling_classes=scrambling_classes,
    ))


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
    return asyncio.run(async_exports._export_from_endpoint(
        sis_settings=sis_settings,
        endpoint=endpoint,
        fp=fp,
        since_ordinal=since_ordinal,
        export_limit=export_limit,
        since=since,
        params=params,
        scrambling_classes=scrambling_classes,
    ))


def export_from_endpoint_generator(
    sis_settings: SupportsExportAuthentication,
    endpoint: str,
    since_ordinal: int = 0,
    export_limit: int = 1000,
    since: str = 'since',
    params: dict | None = None,
    scrambling_classes: list[ScramblingClass] | None = None
) -> Generator[list[dict], None, None]:
    return iterate_async_generator(async_exports.export_from_endpoint_generator(
        sis_settings=sis_settings,
        endpoint=endpoint,
        since_ordinal=since_ordinal,
        export_limit=export_limit,
        since=since,
        params=params,
        scrambling_classes=scrambling_classes,
    ))


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
    return iterate_async_generator(async_exports.export_pages_from_sisu(
        sisu_config,
        resource,
        since_ordinal=since_ordinal,
        params=params,
        scramble=scramble,
        export_limit=export_limit,
    ))


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

    return asyncio.run(async_exports.export_from_sisu(
        sisu_config,
        resource,
        since_ordinal=since_ordinal,
        params=params,
        fp=fp,
        as_generator=False,
        scramble=scramble,
    ))
