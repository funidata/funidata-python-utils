#  Copyright (c) 2025 Funidata Oy.
#  All rights reserved.
# ------------------------------------------------------------------------------
from typing import Literal

from pydantic import BaseModel

from .common import LocalizedString, FinnishAddress, GenericAddress


class Building(BaseModel):
    id: str
    documentState: Literal['ACTIVE', 'DRAFT', 'DELETED']
    universityOrgIds: list[str]
    name: LocalizedString
    addresss: FinnishAddress | GenericAddress
