#  Copyright (c) 2025 Funidata Oy.
#  All rights reserved.
# ------------------------------------------------------------------------------
from typing import Literal

from pydantic import BaseModel, field_validator

from .common import LocalDateRange, LocalizedString


class CurriculumPeriod(BaseModel):
    id: str
    documentState: Literal['ACTIVE', 'DRAFT', 'DELETED']
    universityOrgId: str
    name: LocalizedString
    abbreviation: LocalizedString
    activePeriod: LocalDateRange

    @field_validator('activePeriod')
    def active_period_requires_startDate(cls, val: LocalDateRange) -> LocalDateRange:
        if val.startDate is None:
            raise ValueError('startDate is required')
        return val
