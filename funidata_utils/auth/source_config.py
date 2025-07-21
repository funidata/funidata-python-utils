#  Copyright (c) 2025 Funidata Oy.
#  All rights reserved.
# ------------------------------------------------------------------------------
from typing import ClassVar

from pydantic import BaseModel


class SourceConfig(BaseModel):
    name: ClassVar[str]
    host: str
    proxies: dict | None = None
