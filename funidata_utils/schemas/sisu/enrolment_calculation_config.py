#  Copyright (c) 2026 Funidata Oy.
#  All rights reserved.
# ------------------------------------------------------------------------------
from typing import Annotated, Literal, Union

from pydantic import BaseModel, Field, conset

from funidata_utils.schemas.sisu.base import SisBase
from funidata_utils.schemas.sisu.common import (
    OTM_ID_REGEX_VALIDATED_STR, LocalizedString, STRIPPED_STR, sis_code_urn_pattern, CreditRange,
    SIS_MAX_SMALL_SET_SIZE,
)


class AttainedCreditRangeRule(BaseModel):
    type: Literal['AttainedCreditRange'] = 'AttainedCreditRange'
    educationIds: conset(OTM_ID_REGEX_VALIDATED_STR, max_length=SIS_MAX_SMALL_SET_SIZE)  # noqa
    degreeProgramTypeUrn: Annotated[STRIPPED_STR, Field(pattern=sis_code_urn_pattern('degree-program-type'))] | None = None
    creditRange: CreditRange | None = None
    creditOrder: Literal['NONE', 'ASCENDING', 'DESCENDING']


class CompulsoryFormalPrerequisitesRule(BaseModel):
    type: Literal['CompulsoryFormalPrerequisites'] = 'CompulsoryFormalPrerequisites'


class CourseUnitInPrimaryPlanRule(BaseModel):
    type: Literal['CourseUnitInPrimaryPlan'] = 'CourseUnitInPrimaryPlan'


class EducationRule(BaseModel):
    type: Literal['Education'] = 'Education'
    educationGroupIds: conset(OTM_ID_REGEX_VALIDATED_STR, min_length=1)  # noqa


class EducationTypeRule(BaseModel):
    type: Literal['EducationType'] = 'EducationType'
    educationTypeUrns: conset(Annotated[STRIPPED_STR, Field(pattern=sis_code_urn_pattern('education-type'))], min_length=1)  # noqa


class EnrolmentForCourseUnitRealisationRule(BaseModel):
    type: Literal['EnrolmentForCourseUnitRealisation'] = 'EnrolmentForCourseUnitRealisation'
    courseUnitRealisationIds: conset(OTM_ID_REGEX_VALIDATED_STR, min_length=1)  # noqa


class NotAlreadyEnrolledToAssessmentItemRule(BaseModel):
    type: Literal['NotAlreadyEnrolledToAssessmentItemRule'] = 'NotAlreadyEnrolledToAssessmentItemRule'


class PersonGroupMembershipRule(BaseModel):
    type: Literal['PersonGroupMembership'] = 'PersonGroupMembership'
    personGroupIds: conset(OTM_ID_REGEX_VALIDATED_STR, min_length=1)  # noqa


class RecommendedFormalPrerequisitesRule(BaseModel):
    type: Literal['RecommendedFormalPrerequisites'] = 'RecommendedFormalPrerequisites'


class ValidStudyRightRule(BaseModel):
    type: Literal['ValidStudyRight'] = 'ValidStudyRight'


class ValidTermRegistrationRule(BaseModel):
    type: Literal['ValidTermRegistration'] = 'ValidTermRegistration'


RuleModel = Annotated[
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
        ValidTermRegistrationRule,
    ],
    Field(discriminator='type'),
]


class EnrolmentMaximumUsersQuota(BaseModel):
    size: int
    name: LocalizedString
    quotaPersonRules: list[
        RuleModel
    ]
    id: OTM_ID_REGEX_VALIDATED_STR


class EnrolmentCalculationConfig(SisBase):
    documentState: Literal['ACTIVE', 'DRAFT', 'DELETED']
    id: OTM_ID_REGEX_VALIDATED_STR
    maxSelected: int | None = None
    manualConfirmation: bool
    requirementPersonRules: list[
        RuleModel
    ] | None = None
    orderingPersonRules: list[
        RuleModel
    ] | None = None
    selectedUserQuotas: list[EnrolmentMaximumUsersQuota] | None = None
    maximumUserQuotas: list[EnrolmentMaximumUsersQuota] | None = None
