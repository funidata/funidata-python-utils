#  Copyright (c) 2025 Funidata Oy.
#  All rights reserved.
# ------------------------------------------------------------------------------
from pydantic import BaseModel, conint


class SisExport(BaseModel):
    endpoint: str
    default_export_limit: conint(ge=1, le=5000)


class SisImport(BaseModel):
    endpoint: str
    default_import_limit: conint(ge=1, le=5000) = 1500
