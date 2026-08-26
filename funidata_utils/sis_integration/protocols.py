#  Copyright (c) 2025 Funidata Oy.
#  All rights reserved.
# ------------------------------------------------------------------------------
import typing
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


class ScramblingClass(typing.Protocol):
    def scramble(self, entity) -> dict:
        ...


class SisExportable(Protocol):
    exports: SisExport


class SisExportableSupportScrambling(SisExportable, Protocol):
    scrambling_classes: list[ScramblingClass] | None = None


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
