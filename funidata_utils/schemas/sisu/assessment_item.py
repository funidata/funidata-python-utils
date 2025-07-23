#  Copyright (c) 2025 Funidata Oy.
#  All rights reserved.
# ------------------------------------------------------------------------------
import datetime
from typing import Literal, Annotated

from pydantic import BaseModel, Field, field_serializer

from .common import LocalizedString, CreditRange, sis_code_urn_pattern, OrganisationRoleShareBase


PossibleAttainmentLanguage = Annotated[str, Field(pattern=sis_code_urn_pattern('language'))]


class AssessmentItem(BaseModel):
    id: str
    documentState: Literal['ACTIVE', 'DRAFT', 'DELETED']
    universityOrgId: str
    credits: CreditRange
    name: LocalizedString
    nameSpecifier: LocalizedString | None = None
    gradeScaleId: str
    possibleAttainmentLanguages: list[PossibleAttainmentLanguage] | None = None
    assessmentItemType: sis_code_urn_pattern('assessment-item-type')
    contentDescription: LocalizedString | None = None
    studyFormat: LocalizedString | None = None
    grading: LocalizedString | None = None
    learningMaterial: LocalizedString | None = None
    literature: list[dict] | None = None  # TODO: Define LiteratureName + LiteratureReference
    studyField: Annotated[str, Field(pattern=sis_code_urn_pattern('study-field'))]
    subject: Annotated[str, Field(pattern=sis_code_urn_pattern('subject'))]
    snapshotDateTime: datetime.datetime | None = None
    responsibilityInfos: list[dict] | None = None  # TODO: PersonWithModuleResponsibilityType
    organisations: list[OrganisationRoleShareBase]
    primaryCourseUnitGroupId: str
    cooperationNetworkDetails: dict | None = None  # TODO: CooperationNetworkDetails
    rdiCreditsEnabled: bool

    @field_serializer('snapshotDateTime')
    def serialize_ssdt(self, ssdt: datetime.datetime | None, _info):
        if ssdt is None:
            return None

        return ssdt.strftime("%Y-%m-%dT%H:%M:%S")
