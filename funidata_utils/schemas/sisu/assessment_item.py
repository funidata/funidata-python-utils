#  Copyright (c) 2025 Funidata Oy.
#  All rights reserved.
# ------------------------------------------------------------------------------
import datetime
from typing import Literal, Annotated

from pydantic import BaseModel, Field, field_serializer, conlist

from .common import (
    PersonWithModuleResponsibilityInfoType,
    SIS_MAX_MEDIUM_SET_SIZE,
    LocalizedString,
    CreditRange,
    sis_code_urn_pattern,
    OrganisationRoleShareBase,
    STRIPPED_STR,
    OTM_ID_REGEX_VALIDATED_STR,
)


PossibleAttainmentLanguage = Annotated[STRIPPED_STR, Field(pattern=sis_code_urn_pattern('language'))]


class AssessmentItem(BaseModel):
    id: OTM_ID_REGEX_VALIDATED_STR
    documentState: Literal['ACTIVE', 'DRAFT', 'DELETED']
    universityOrgIds: conlist(OTM_ID_REGEX_VALIDATED_STR, min_length=1, max_length=1)
    credits: CreditRange
    name: LocalizedString
    nameSpecifier: LocalizedString | None = None
    gradeScaleId: str
    possibleAttainmentLanguages: list[PossibleAttainmentLanguage] | None = None
    assessmentItemType: Annotated[STRIPPED_STR, Field(pattern=sis_code_urn_pattern('assessment-item-type'))]
    contentDescription: LocalizedString | None = None
    studyFormat: LocalizedString | None = None
    grading: LocalizedString | None = None
    learningMaterial: LocalizedString | None = None
    literature: list[dict] | None = None  # TODO: Define LiteratureName + LiteratureReference
    studyField: Annotated[STRIPPED_STR, Field(pattern=sis_code_urn_pattern('study-field'))] | None = None
    subject: Annotated[STRIPPED_STR, Field(pattern=sis_code_urn_pattern('subject'))] | None = None
    snapshotDateTime: datetime.datetime | None = None
    responsibilityInfos: conlist(PersonWithModuleResponsibilityInfoType, max_length=SIS_MAX_MEDIUM_SET_SIZE) | None = None
    organisations: list[OrganisationRoleShareBase]
    primaryCourseUnitGroupId: OTM_ID_REGEX_VALIDATED_STR
    cooperationNetworkDetails: dict | None = None  # TODO: CooperationNetworkDetails
    rdiCreditsEnabled: Literal['ENABLED', 'DISABLED']

    @field_serializer('snapshotDateTime')
    def serialize_ssdt(self, ssdt: datetime.datetime | None, _info):
        if ssdt is None:
            return None

        return ssdt.strftime("%Y-%m-%dT%H:%M:%S")
