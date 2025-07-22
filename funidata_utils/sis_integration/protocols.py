#  Copyright (c) 2025 Funidata Oy.
#  All rights reserved.
# ------------------------------------------------------------------------------
from typing import Protocol, runtime_checkable

from .resources.schemas import SisExport, SisImport


class SisExportable(Protocol):
    exports: SisExport


class SisImportable(Protocol):
    imports: SisImport


@runtime_checkable
class SisLegacyImportable(Protocol):
    legacy_imports: SisImport


class SisPatchable(Protocol):
    patches: SisImport


@runtime_checkable
class SisLegacyPatchable(Protocol):
    legacy_patches: SisImport
