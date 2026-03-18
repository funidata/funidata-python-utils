from typing import Annotated, Literal, Union

from pydantic import BaseModel, Field, conset

from funidata_utils.schemas.sisu.base import SisBase
from funidata_utils.schemas.sisu.common import (
    OTM_ID_REGEX_VALIDATED_STR, LocalizedString, STRIPPED_STR, sis_code_urn_pattern, CreditRange,
    SIS_MAX_SMALL_SET_SIZE,
)


class BaseRule(BaseModel):
    type: Literal[
        'ValidStudyRight',
        'ValidTermRegistration',
        'PersonGroupMembership',
        'CourseUnitInPrimaryPlan',
        'CompulsoryFormalPrerequisites',
        'RecommendedFormalPrerequisites',
        'AttainedCreditRange',
        'EnrolmentForCourseUnitRealisation',
        'NotAlreadyEnrolledToAssessmentItemRule',
        'EducationType',
        'Education'
    ]


class AttainedCreditRangeRule(BaseRule):
    educationIds: conset(OTM_ID_REGEX_VALIDATED_STR, max_length=SIS_MAX_SMALL_SET_SIZE)  # noqa
    degreeProgrammeTypeUrn: Annotated[STRIPPED_STR, Field(pattern=sis_code_urn_pattern('degree-program-type'))] | None
    creditRange: CreditRange | None = None
    creditOrder: Literal['NONE', 'ASCENDING', 'DESCENDING']


class CompulsoryFormalPrerequisitesRule(BaseRule):
    ...


class CourseUnitInPrimaryPlanRule(BaseRule):
    ...


class EducationRule(BaseRule):
    educationGroupIds: conset(OTM_ID_REGEX_VALIDATED_STR, min_length=1)  # noqa


class EducationTypeRule(BaseRule):
    educationTypeUrns: conset(Annotated[STRIPPED_STR, Field(pattern=sis_code_urn_pattern('education-type'))], min_length=1)  # noqa


class EnrolmentForCourseUnitRealisationRule(BaseRule):
    courseUnitRealisationIds: conset(OTM_ID_REGEX_VALIDATED_STR, min_length=1)  # noqa


class NotAlreadyEnrolledToAssessmentItemRule(BaseRule):
    ...


class PersonGroupMembershipRule(BaseRule):
    personGroupIds: conset(OTM_ID_REGEX_VALIDATED_STR, min_length=1)  # noqa


class RecommendedFormalPrerequisitesRule(BaseRule):
    ...


class ValidStudyRightRule(BaseRule):
    ...


class ValidTermRegistrationRule(BaseRule):
    ...


class EnrolmentMaximumUsersQuota(BaseModel):
    size: int
    name: LocalizedString
    quotaPersonRules: list[
        Union[
            AttainedCreditRangeRule,
            CompulsoryFormalPrerequisitesRule,
            CourseUnitInPrimaryPlanRule,
            EducationRule,
            EducationTypeRule,
            EnrolmentForCourseUnitRealisationRule,
            NotAlreadyEnrolledToAssessmentItemRule,
            PersonGroupMembershipRule,
            RecommendedFormalPrerequisitesRule,
            ValidStudyRightRule,
            ValidTermRegistrationRule
        ]
    ]
    id: OTM_ID_REGEX_VALIDATED_STR


class EnrolmentCalculationConfig(SisBase):
    documentState: Literal['ACTIVE', 'DRAFT', 'DELETED']
    id: OTM_ID_REGEX_VALIDATED_STR
    maxSelected: int | None = None
    manualConfirmation: bool
    requirementPersonRules: list[
        Union[
            AttainedCreditRangeRule,
            CompulsoryFormalPrerequisitesRule,
            CourseUnitInPrimaryPlanRule,
            EducationRule,
            EducationTypeRule,
            EnrolmentForCourseUnitRealisationRule,
            NotAlreadyEnrolledToAssessmentItemRule,
            PersonGroupMembershipRule,
            RecommendedFormalPrerequisitesRule,
            ValidStudyRightRule,
            ValidTermRegistrationRule
        ]
    ] | None = None
    orderingPersonRules: list[
        Union[
            AttainedCreditRangeRule,
            CompulsoryFormalPrerequisitesRule,
            CourseUnitInPrimaryPlanRule,
            EducationRule,
            EducationTypeRule,
            EnrolmentForCourseUnitRealisationRule,
            NotAlreadyEnrolledToAssessmentItemRule,
            PersonGroupMembershipRule,
            RecommendedFormalPrerequisitesRule,
            ValidStudyRightRule,
            ValidTermRegistrationRule
        ]
    ] | None = None
    selectedUserQuotas: list[EnrolmentMaximumUsersQuota] | None = None
    maximumUserQuotas: list[EnrolmentMaximumUsersQuota] | None = None
