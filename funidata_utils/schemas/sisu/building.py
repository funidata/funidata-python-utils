#  Copyright (c) 2025 Funidata Oy.
#  All rights reserved.
# ------------------------------------------------------------------------------
from typing import Literal

from pydantic import BaseModel

from .common import LocalizedString, FinnishAddress, GenericAddress, OTM_ID_REGEX_VALIDATED_STR


class Building(BaseModel):
    id: OTM_ID_REGEX_VALIDATED_STR
    documentState: Literal['ACTIVE', 'DRAFT', 'DELETED']
    universityOrgIds: list[str]
    name: LocalizedString
    addresss: FinnishAddress | GenericAddress
