#  Copyright (c) 2025 Funidata Oy.
#  All rights reserved.
# ------------------------------------------------------------------------------

from typing import Literal, Annotated

from pydantic import BaseModel, Field

from .common import LocalDateRange, sis_code_urn_pattern, STRIPPED_STR, OTM_ID_REGEX_VALIDATED_STR


class MobilityPeriod(BaseModel):
    id: OTM_ID_REGEX_VALIDATED_STR
    documentState: Literal['ACTIVE', 'DRAFT', 'DELETED']
    studyRightId: str
    personId: str
    mobilityDirection: Literal['INBOUND', 'OUTBOUND']
    activityPeriod: LocalDateRange
    phase: Literal['PHASE1', 'PHASE2']
    mobilityProgramUrn: Annotated[STRIPPED_STR, Field(pattern=sis_code_urn_pattern('mobility-program'))]
    mobilityProgramDescription: str | None = None
    mobilityTypeUrn: Annotated[STRIPPED_STR, Field(pattern=sis_code_urn_pattern('mobility-type'))]
    countryUrn: Annotated[STRIPPED_STR, Field(pattern=sis_code_urn_pattern('country'))]
    internationalInstitutionUrn: Annotated[STRIPPED_STR | None, Field(pattern=sis_code_urn_pattern('international-institution'))] = None
    organisation: str | None = None
    mobilityStudyRightTypeUrn: Annotated[STRIPPED_STR | None, Field(pattern=sis_code_urn_pattern('mobility-study-right-type'))] = None
    virtualMobilityType: Literal["None", "RemoteAttendance", "BlendedAttendance"] | None = None
    isCancelled: bool
