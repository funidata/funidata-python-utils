#  Copyright (c) 2025 Funidata Oy.
#  All rights reserved.
# ------------------------------------------------------------------------------
from typing import Protocol

from .resources.schemas import SisExport, SisImport


class SisExportable(Protocol):
    exports: SisExport


class SisImportable(Protocol):
    imports: SisImport


class SisLegacyImportable(Protocol):
    legacy_imports: SisImport


class SisPatchable(Protocol):
    patches: SisImport


class SisLegacyPatchable(Protocol):
    legacy_patches: SisImport
