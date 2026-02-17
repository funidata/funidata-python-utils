#  Copyright (c) 2025 Funidata Oy.
#  All rights reserved.
# ------------------------------------------------------------------------------
import datetime
from typing import Literal

from funidata_utils.schemas.sisu.common import OTM_ID_REGEX_VALIDATED_STR
from pydantic import BaseModel, field_serializer


class StudyTermLocator(BaseModel):
    studyYearStartYear: int
    termIndex: int


class TermRegistration(BaseModel):
    localId: str
    studyTerm: StudyTermLocator
    registrationDate: datetime.date
    termRegistrationType: Literal['ATTENDING', 'NONATTENDING', 'MISSING', 'NEGLECTED']
    previousRegistrationType: Literal['ATTENDING', 'NONATTENDING', 'MISSING', 'NEGLECTED'] | None = None
    previousRegistrationDate: datetime.date | None = None
    statutoryAbsence: bool | None = None
    statutoryAbsenceDate: datetime.date | None = None
    statutoryAbsenceChangedBy: OTM_ID_REGEX_VALIDATED_STR | None = None
    tuitionFeePaymentState: Literal['PAID', 'OUTSTANDING'] | None = None

    @field_serializer('statutoryAbsenceDate', 'previousRegistrationDate', 'registrationDate')
    def serialize_date_fields(self, _date: datetime.date | None, _info):
        if _date is None:
            return None

        return _date.isoformat()


class StudyRightStatePeriod(BaseModel):
    state: Literal[
        'NOT_STARTED', 'ACTIVE', 'ACTIVE_NONATTENDING', 'GRADUATED', 'RESCINDED', 'CANCELLED_BY_ADMINISTRATION', 'TENTATIVE', 'DENIED', 'PASSIVE', 'EXPIRED'
    ]
    startDate: datetime.date | None = None
    endDate: datetime.date | None = None

    @field_serializer('startDate', 'endDate')
    def serialize_date_fields(self, _date: datetime.date | None, _info):
        if _date is None:
            return None

        return _date.isoformat()


class StudyRightTermRegistrations(BaseModel):
    documentState: Literal['ACTIVE', 'DRAFT', 'DELETED']
    studyRightId: OTM_ID_REGEX_VALIDATED_STR
    studentId: OTM_ID_REGEX_VALIDATED_STR
    termRegistrations: list[TermRegistration]
    statePeriodOverrides: list[StudyRightStatePeriod] | None
