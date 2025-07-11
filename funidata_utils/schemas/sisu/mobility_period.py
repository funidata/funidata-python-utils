#  Copyright (c) 2025 Funidata Oy.
#  All rights reserved.
# ------------------------------------------------------------------------------

from typing import Literal

from pydantic import BaseModel, constr

from .study_right import LocalDateRange


class MobilityPeriod(BaseModel):
    id: str
    documentState: Literal['ACTIVE', 'DRAFT', 'DELETED']
    studyRightId: str
    personId: str
    mobilityDirection: Literal['INBOUND', 'OUTBOUND']
    activityPeriod: LocalDateRange
    phase: Literal['PHASE1', 'PHASE2']
    mobilityProgramUrn: constr(pattern='(urn:code:mobility-program)(:[A-z_0-9]+)*', strip_whitespace=True)
    mobilityProgramDescription: str | None = None
    mobilityTypeUrn: constr(pattern='(urn:code:mobility-type)(:[A-z_0-9]+)*', strip_whitespace=True)
    countryUrn: constr(pattern='(urn:code:country)(:[A-z_0-9]+)*', strip_whitespace=True)
    internationalInstitutionUrn: constr(pattern='(urn:code:international-institution)(:[A-z_0-9]+)*', strip_whitespace=True) | None = None
    organisation: str | None = None
    mobilityStudyRightTypeUrn: constr(pattern='(urn:code:mobility-study-right-type)(:[A-z_0-9]+)*', strip_whitespace=True) | None = None
    virtualMobilityType: Literal["None", "RemoteAttendance", "BlendedAttendance"] | None = None
    isCancelled: bool
