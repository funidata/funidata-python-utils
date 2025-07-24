#  Copyright (c) 2025 Funidata Oy.
#  All rights reserved.
# ------------------------------------------------------------------------------
from typing import Annotated

from pydantic import BaseModel, conlist, field_validator, Field

from .common import LocalDateRange, LocalizedString, SIS_MAX_SMALL_SET_SIZE


class StudyPeriodTemplate(BaseModel):
    defaultValid: LocalDateRange
    overrideValidities: conlist(LocalDateRange, max_length=100) | None = None  # hardcoded in Sisu to 100 at time of writing
    name: LocalizedString
    size: Annotated[int, Field(ge=1, le=100)]  # hardcoded values in Sisu at time of writing
    visibleByDefault: bool = False
    includedInTargetCreditsCalculation: bool = False

    @field_validator('defaultValid')
    def default_valid_requires_startDate(cls, val: LocalDateRange) -> LocalDateRange:
        if val.startDate is None:
            raise ValueError('startDate is required')
        return val


class StudyTermTemplate(BaseModel):
    valid: LocalDateRange
    name: LocalizedString
    studyPeriods: conlist(StudyPeriodTemplate, min_length=1, max_length=SIS_MAX_SMALL_SET_SIZE)


class StudyYearTemplate(BaseModel):
    id: str
    valid: LocalDateRange
    org: str
    studyTerms: conlist(StudyTermTemplate, min_length=1, max_length=SIS_MAX_SMALL_SET_SIZE)
