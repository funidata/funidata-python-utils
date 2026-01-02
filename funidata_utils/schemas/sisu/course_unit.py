#  Copyright (c) 2025 Funidata Oy.
#  All rights reserved.
# ------------------------------------------------------------------------------

import datetime
from typing import Literal, Annotated, Self

from pydantic import BaseModel, Field, field_serializer, conlist, model_validator, ValidationError

from .base import SisBase
from .common import (
    sis_code_urn_pattern, STRIPPED_STR, LocalizedString, OTM_ID_REGEX_VALIDATED_STR, SIS_MAX_SMALL_SET_SIZE, LocalDateRange,
    SIS_MAX_MEDIUM_SET_SIZE, SIS_MAX_BIG_SET_SIZE, STRING_WITH_3_SLASHES, OrganisationRoleShare, PersonWithModuleResponsibilityInfoType,
)


class CreditRange(BaseModel):
    min: float
    max: float | None = None


class IntRange(BaseModel):
    min: int
    max: int | None = None


class StudyYearRange(BaseModel):
    start: Annotated[int, Field(gt=0, lt=10000)]
    end: Annotated[int, Field(gt=0, lt=10000)]


class CompletionMethodRepeat(BaseModel):
    studyYearRange: StudyYearRange
    yearInterval: Annotated[int | None, Field(gt=0)] = None
    repeatPossibility: conlist(STRING_WITH_3_SLASHES, min_length=1, max_length=SIS_MAX_SMALL_SET_SIZE)


class CompletionMethod(BaseModel):
    localId: str
    description: LocalizedString | None = None
    studyType: Literal['DEGREE_STUDIES', 'OPEN_UNIVERSITY_STUDIES', 'SEPARATE_STUDIES']
    assessmentItemOptionalityDescription: LocalizedString | None = None
    automaticEvaluation: bool | None = None
    require: IntRange | None = None
    typeOfRequire: Literal['OPTIONAL_WITH_REQUIRE_RANGE', 'OPTIONAL_WITH_DESCRIPTION', 'ALL_SELECTED_REQUIRED']
    assessmentItemIds: conlist(OTM_ID_REGEX_VALIDATED_STR, min_length=1, max_length=SIS_MAX_SMALL_SET_SIZE)
    repeats: conlist(CompletionMethodRepeat, max_length=SIS_MAX_SMALL_SET_SIZE) | None = None
    evaluationCriteria: LocalizedString | None = None
    prerequisites: LocalizedString | None = None


class CourseUnitSubstitution(BaseModel):
    courseUnitGroupId: OTM_ID_REGEX_VALIDATED_STR
    credits: Annotated[float | None, Field(ge=1)] = None


class LiteratureName(BaseModel):
    localId: str
    type: str
    name: str


class LiteratureReference(BaseModel):
    localId: str
    type: str
    url: str


class CourseUnitPrerequisite(BaseModel):
    type: str
    courseUnitGroupId: OTM_ID_REGEX_VALIDATED_STR


class ModulePrerequisite(BaseModel):
    type: str
    moduleGroupId: OTM_ID_REGEX_VALIDATED_STR


class PrerequisiteGroup(BaseModel):
    prerequisites: list[CourseUnitPrerequisite | ModulePrerequisite] | None = None


class CooperationNetworkShare(BaseModel):
    cooperationNetworkId: OTM_ID_REGEX_VALIDATED_STR | None = None
    validityPeriod: LocalDateRange | None = None


class CooperationNetworkDetails(BaseModel):
    direction: Literal['INBOUND', 'OUTBOUND', 'NONE']
    networks: list[CooperationNetworkShare] | None = None
    externalId: str
    outboundStatus: Literal['NOT_VALID', 'FORWARDED', 'RECORDED', 'REJECTED'] | None = None
    outboundStatusTime: datetime.datetime | None = None
    outboundStatusMessage: str | None = None

    @field_serializer('outboundStatusTime')
    def serialize_ssdt(self, ssdt: datetime.datetime | None, _info):
        if ssdt is None:
            return None

        return ssdt.strftime("%Y-%m-%dT%H:%M:%S")


class CourseUnit(SisBase):
    documentState: Literal['ACTIVE', 'DRAFT', 'DELETED']
    id: OTM_ID_REGEX_VALIDATED_STR
    universityOrgIds: conlist(OTM_ID_REGEX_VALIDATED_STR, max_length=SIS_MAX_SMALL_SET_SIZE)
    groupId: OTM_ID_REGEX_VALIDATED_STR
    approvalState: Literal[
                       'urn:code:approval-state-type:not-ready',
                       'urn:code:approval-state-type:ready-for-approval',
                       'urn:code:approval-state-type:not-approved',
                       'urn:code:approval-state-type:approved',
                   ] | None = None
    credits: CreditRange
    completionMethods: conlist(CompletionMethod, max_length=SIS_MAX_MEDIUM_SET_SIZE) | None = None
    assessmentItemOrder: conlist(OTM_ID_REGEX_VALIDATED_STR, max_length=SIS_MAX_BIG_SET_SIZE) | None = None
    substitutions: conlist(list[CourseUnitSubstitution], max_length=SIS_MAX_MEDIUM_SET_SIZE) | None = None
    name: LocalizedString
    code: str
    abbreviation: str | None = None
    validityPeriod: LocalDateRange
    gradeScaleId: OTM_ID_REGEX_VALIDATED_STR
    tweetText: LocalizedString | None = None
    outcomes: LocalizedString | None = None
    prerequisites: LocalizedString | None = None
    content: LocalizedString | None = None
    additional: LocalizedString | None = None
    learningMaterial: LocalizedString | None = None
    literature: conlist(LiteratureName | LiteratureReference, max_length=SIS_MAX_MEDIUM_SET_SIZE) | None = None
    searchTags: conlist(str, max_length=SIS_MAX_MEDIUM_SET_SIZE) | None = None
    categoryTags: conlist(Annotated[str, Field(pattern=sis_code_urn_pattern('category-tag'))], max_length=SIS_MAX_MEDIUM_SET_SIZE) | None = None
    recommendedFormalPrerequisites: conlist(PrerequisiteGroup, max_length=SIS_MAX_MEDIUM_SET_SIZE) | None = None
    compulsoryFormalPrerequisites: conlist(PrerequisiteGroup, max_length=SIS_MAX_MEDIUM_SET_SIZE) | None = None
    studyFields: conlist(Annotated[str, Field(pattern=sis_code_urn_pattern('study-field'))], max_length=SIS_MAX_SMALL_SET_SIZE, min_length=1)
    studyLevel: Annotated[STRIPPED_STR, Field(pattern=sis_code_urn_pattern('study-level'))]
    courseUnitType: Annotated[STRIPPED_STR, Field(pattern=sis_code_urn_pattern('course-unit-type'))]
    subject: Annotated[str | None, Field(pattern=sis_code_urn_pattern('subject'))] = None
    cefrLevel: Annotated[str | None, Field(pattern=sis_code_urn_pattern('cefr-level'))] = None
    responsibilityInfos: conlist(PersonWithModuleResponsibilityInfoType, min_length=1, max_length=SIS_MAX_MEDIUM_SET_SIZE)
    organisations: conlist(OrganisationRoleShare, max_length=SIS_MAX_MEDIUM_SET_SIZE, min_length=1)
    possibleAttainmentLanguages: conlist(
        Annotated[STRIPPED_STR, Field(pattern=sis_code_urn_pattern('language'))],
        max_length=SIS_MAX_MEDIUM_SET_SIZE,
        min_length=1
    )
    equivalentCoursesInfo: LocalizedString | None = None
    curriculumPeriodIds: conlist(OTM_ID_REGEX_VALIDATED_STR, max_length=SIS_MAX_MEDIUM_SET_SIZE, min_length=1)
    customCodeUrns: Annotated[dict[str, list[str]] | None, Field(min_length=1)] = None
    inclusionApplicationInstruction: LocalizedString | None = None
    cooperationNetworkDetails: CooperationNetworkDetails | None = None
    s2r2Classification: Annotated[str | None, Field(pattern=sis_code_urn_pattern('s2r2-classification'))] = None
    rdiCreditsEnabled: Literal['ENABLED', 'DISABLED']
