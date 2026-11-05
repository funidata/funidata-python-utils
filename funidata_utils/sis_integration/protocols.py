#  Copyright (c) 2025 Funidata Oy.
#  All rights reserved.
# ------------------------------------------------------------------------------
from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from .resources.schemas import SisExport, SisImport, SisDelete


class HasHostAndProxies(Protocol):
    host: str
    proxies: dict | None


class SupportsIntegrationAuthentication(HasHostAndProxies, Protocol):
    def get_integration_auth(self) -> tuple[str, str]:
        ...


class SupportsExportAuthentication(HasHostAndProxies, Protocol):
    def get_export_auth(self) -> tuple[str, str]:
        ...


class ScramblingClass(Protocol):
    """
    A scrambler as used by the export functions. Scramblers are usually passed as classes
    (`scramble` is a classmethod on `SingletonMetaScrambler`), but an instance with a plain
    `scramble` method satisfies this too.
    """
    scrambling_keys: dict

    @classmethod
    def scramble(cls, entity: dict, processed_keys: set) -> dict:
        ...


class SisExportable(Protocol):
    exports: SisExport


class SisExportableSupportScrambling(SisExportable, Protocol):
    @property
    def scrambling_classes(self) -> Sequence[type[ScramblingClass]] | None:
        ...


@runtime_checkable
class SisImportable(Protocol):
    imports: SisImport


@runtime_checkable
class SisDeletable(Protocol):
    delete: SisDelete


@runtime_checkable
class SisLegacyImportable(Protocol):
    legacy_imports: SisImport


@runtime_checkable
class SisPatchable(Protocol):
    patches: SisImport


@runtime_checkable
class SisLegacyPatchable(Protocol):
    legacy_patches: SisImport
