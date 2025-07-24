#  Copyright (c) 2025 Funidata Oy.
#  All rights reserved.
# ------------------------------------------------------------------------------
from typing import Annotated

from pydantic import BaseModel, Field


class SisExport(BaseModel):
    endpoint: str
    default_export_limit: Annotated[int, Field(ge=1, le=5000)]


class SisImport(BaseModel):
    endpoint: str
    default_import_limit: Annotated[int, Field(ge=1, le=5000)] = 1500
