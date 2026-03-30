from __future__ import annotations

from datetime import date, datetime
from typing import Annotated, Literal, Union

from pydantic import BaseModel, Field, conset, conlist, field_serializer, field_validator

from funidata_utils.schemas.common_serializers import serialize_as_list
from funidata_utils.schemas.sisu.base import SisBase, HashableBaseModel
from funidata_utils.schemas.sisu.common import (
    LocalDateRange, LocalDateTimeRange, OTM_ID_REGEX_VALIDATED_STR, sis_code_urn_pattern,
    STRIPPED_STR, IntRange, SIS_MAX_MEDIUM_SET_SIZE, OrganisationRoleShare, SIS_MAX_SMALL_SET_SIZE,
    LocalizedString,
)
from funidata_utils.schemas.sisu.course_unit import CooperationNetworkDetails


TWEET_TEXT_MAX_LENGTH = 160

class LiteratureName(HashableBaseModel):
    localId: str
    type: Literal["LiteratureName"]
    name: str


class LiteratureReference(HashableBaseModel):
    localId: str
    type: Literal["LiteratureReference"]
    url: str


Literature = Annotated[
    Union[LiteratureName, LiteratureReference],
    Field(discriminator="type"),
]


class LearningEnvironment(HashableBaseModel):
    primary: bool | None = None
    language: str
    name: str | None = None
    url: str


class StudySubGroup(BaseModel):
    id: str
    name: LocalizedString
    studyEventIds: conset(OTM_ID_REGEX_VALIDATED_STR, max_length=SIS_MAX_MEDIUM_SET_SIZE) | None = None  # noqa
    teacherIds: conset(OTM_ID_REGEX_VALIDATED_STR, max_length=SIS_MAX_MEDIUM_SET_SIZE) | None = None  # noqa
    cancelled: bool | None = None
    size: int | None = None
    externalId: str | None = None

    @field_serializer("studyEventIds", "teacherIds")
    def serialize_set_as_list(self, v, _info) -> list[str] | None:
        serialized_list = serialize_as_list(v)
        return serialized_list


class StudyGroupSet(BaseModel):
    localId: str
    name: LocalizedString
    studySubGroups: list[StudySubGroup]
    subGroupRange: IntRange


class PersonWithCourseUnitResponsibilityInfoType(BaseModel):
    text: LocalizedString | None = None
    personId: OTM_ID_REGEX_VALIDATED_STR | None = None
    roleUrn: Literal[
        'urn:code:course-unit-realisation-responsibility-info-type:responsible-teacher',
        'urn:code:course-unit-realisation-responsibility-info-type:teacher',
        'urn:code:course-unit-realisation-responsibility-info-type:administrative-person',
        'urn:code:course-unit-realisation-responsibility-info-type:contact-info'
    ]
    validity: LocalDateRange | None = None
    validityPeriod: LocalDateRange | None = None


class LocalizedLink(BaseModel):
    url: LocalizedString | None = None
    label: LocalizedString | None = None


class CopyDetails(BaseModel):
    sourceCourseUnitRealisationId: OTM_ID_REGEX_VALIDATED_STR
    copyTargetStudyYear: LocalDateRange


class CourseUnitRealisation(SisBase):
    documentState: Literal['ACTIVE', 'DRAFT', 'DELETED']
    id: OTM_ID_REGEX_VALIDATED_STR
    universityOrgIds: conlist(OTM_ID_REGEX_VALIDATED_STR, min_length=1, max_length=1)  # noqa
    flowState: Literal['NOT_READY', 'PUBLISHED', 'CANCELLED', 'ARCHIVED'] | None = None
    massExamSessionId: OTM_ID_REGEX_VALIDATED_STR | None = None
    massExamSessionName: LocalizedString | None = None
    name: LocalizedString
    nameSpecifier: LocalizedString
    assessmentItemIds: conset(OTM_ID_REGEX_VALIDATED_STR, min_length=1, max_length=SIS_MAX_MEDIUM_SET_SIZE)  # noqa
    tweetText: LocalizedString | None = None
    literature: conset(Literature, max_length=SIS_MAX_MEDIUM_SET_SIZE) | None = None  # noqa
    learningMaterial: LocalizedString | None = None
    learningEnvironmentDescription: LocalizedString | None = None
    learningEnvironments: conset(LearningEnvironment, max_length=SIS_MAX_SMALL_SET_SIZE) | None = None  # noqa
    studyFormat: LocalizedString | None = None
    additionalInfo: LocalizedString | None = None
    publishDate: date
    activityPeriod: LocalDateRange
    teachingLanguageUrn: Annotated[STRIPPED_STR, Field(pattern=sis_code_urn_pattern('language'))] | None = None
    courseUnitRealisationTypeUrn: Annotated[STRIPPED_STR, Field(pattern=sis_code_urn_pattern('course-unit-realisation-type'))]
    studyGroupSets: list[StudyGroupSet]
    responsibilityInfos: conlist(PersonWithCourseUnitResponsibilityInfoType, max_length=SIS_MAX_MEDIUM_SET_SIZE)  # noqa
    organisations: conlist(OrganisationRoleShare, min_length=1, max_length=SIS_MAX_MEDIUM_SET_SIZE)  # noqa
    enrolmentPeriod: LocalDateTimeRange | None = None
    lateEnrolmentEnd: datetime | None = None
    enrolmentAdditionalCancellationEnd: datetime | None = None
    externalEnrolmentLink: LocalizedLink | None = None
    usesExternalEnrolment: bool | None = None
    customCodeUrns: Annotated[dict[str, list[str]], Field(min_length=1)] | None = None
    classificationCodeUrns: Annotated[dict[str, list[str]], Field(min_length=1)] | None = None
    continuousEnrolment: bool | None = None
    externalStructureLink: LocalizedLink | None = None
    usesExternalStructure: bool | None = None
    confirmedStudySubGroupModificationAllowed: bool | None = None
    confirmedStudySubGroupModificationEnd: datetime | None = None
    cooperationNetworkDetails: CooperationNetworkDetails | None = None
    copyDetails: CopyDetails | None = None

    @field_validator('tweetText')
    def tweet_text_max_len(cls, val: LocalizedString | None) -> LocalizedString | None:
        if val is None:
            return None
        if len(val.fi) > TWEET_TEXT_MAX_LENGTH or len(val.sv) > TWEET_TEXT_MAX_LENGTH or len(val.en) > TWEET_TEXT_MAX_LENGTH:
            raise ValueError('Tweet text exceeds max length')
        return val

    @field_serializer("literature", "learningEnvironments")
    def serialize_set_as_list(self, v, _info) -> list[dict] | None:
        serialized_list = serialize_as_list(v)
        return serialized_list

    @field_serializer("assessmentItemIds")
    def serialize_set_as_list_str(self, v, _info) -> list[str] | None:
        serialized_list = serialize_as_list(v)
        return serialized_list

    @field_serializer('lateEnrolmentEnd', 'enrolmentAdditionalCancellationEnd', 'confirmedStudySubGroupModificationEnd')
    def serialize_date_time_as_str(self, dt: datetime | None, _info):
        if dt is None:
            return dt
        return dt.isoformat()

    @field_serializer('publishDate')
    def serialize_date_as_str(self, dt: date | None, _info):
        if dt is None:
            return dt
        return dt.isoformat()
