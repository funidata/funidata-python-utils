#  Copyright (c) 2025 Funidata Oy.
#  All rights reserved.
# ------------------------------------------------------------------------------
from typing import Literal

from pydantic import BaseModel

from .common import LocalizedString, LocalDateRange, OTM_ID_REGEX_VALIDATED_STR


class Grade(BaseModel):
    passed: bool = False
    name: LocalizedString
    abbreviation: LocalizedString
    numericCorrespondence: float


class GradeScale(BaseModel):
    id: OTM_ID_REGEX_VALIDATED_STR
    documentState: Literal['ACTIVE', 'DRAFT', 'DELETED']
    grades: list[Grade]
    validityPeriod: LocalDateRange
    additionalInfo: LocalizedString | None = None
    helpText: LocalizedString | None = None
    name: LocalizedString
    abbreviation: LocalizedString
