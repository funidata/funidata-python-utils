import datetime
from abc import ABC
from typing import Literal, Annotated

from pydantic import BaseModel, conlist, constr, Field, model_validator, field_validator, conset, field_serializer, AfterValidator

from src.schemas.sisu.common import LocalizedString, SIS_MAX_MEDIUM_SET_SIZE, SIS_MAX_MEDIUM_STRING_LENGTH, OTM_ID_REGEX_PATTERN, HashableBaseModel
from src.utils import group_by


class ObjectWithDocumentState(BaseModel):
    documentState: Literal['ACTIVE', 'DRAFT', 'DELETED']


class AttainmentNode(BaseModel, ABC):
    type: Literal['AttainmentReferenceNode', 'AttainmentGroupNode']


class AttainmentGroupNode(AttainmentNode):
    type: Literal['AttainmentGroupNode'] = 'AttainmentGroupNode'
    name: LocalizedString
    nodes: list[AttainmentNode]


class AttainmentReferenceNode(AttainmentNode):
    type: Literal['AttainmentReferenceNode'] = 'AttainmentReferenceNode'
    attainmentId: str


class OrganisationRoleShareBase(HashableBaseModel):
    organisationId: str
    educationalInstitutionUrn: constr(pattern='(urn:code:educational-institution)(:[A-z_0-9]+)*') | None = None
    roleUrn: constr(pattern='(urn:code:organisation-role)(:[A-z_0-9]+)*')
    share: Annotated[float, Field(strict=False, ge=0, le=1)]


class PersonWithAttainmentAcceptorType(HashableBaseModel):
    text: LocalizedString | None = None
    personId: str | None = Field(default=None, description='PublicPersonId', pattern=OTM_ID_REGEX_PATTERN)
    roleUrn: constr(pattern='(urn:code:attainment-acceptor-type)(:[A-z_0-9]+)*')
    title: LocalizedString | None = None

    @model_validator(mode='after')
    def text_or_person_validator(self):
        if self.text is None and self.personId is None:
            raise ValueError('One of text or personId must be specified')

        return self


class GradeAverage(BaseModel):
    gradeScaleId: str
    value: float | None = None
    totalIncludedCredits: float
    method: Literal[
        'COURSE_UNIT_ARITHMETIC_MEAN_WEIGHTING_BY_CREDITS',
        'COURSE_UNIT_AND_EMPTY_MODULE_ARITHMETIC_MEAN_WEIGHTED_BY_CREDITS',
        'ARITHMETIC_MEAN_WEIGHTING_BY_CREDITS'
    ]


class CreditTransferInfo(BaseModel):
    educationalInstitutionUrn: constr(pattern='(urn:code:educational-institution)(:[A-z_0-9]+)*')
    internationalInstitutionUrn: constr(pattern='(urn:code:international-institution)(:[A-z_0-9]+)*') | None = None
    organisation: str | None = None
    creditTransferDate: datetime.date

    @field_serializer('creditTransferDate')
    def date_as_isoformat(self, val: datetime.date, _info):
        return val.isoformat()


class Attainment(ObjectWithDocumentState):
    id: str
    personId: str = Field(description='PrivatePersonId')
    verifierPersonId: str | None = Field(default=None, description='PublicPersonId', pattern=OTM_ID_REGEX_PATTERN)
    studyRightId: str | None = None
    registrationDate: str
    expiryDate: str | None = None
    attainmentLanguageUrn: constr(pattern='(urn:code:language)(:[A-z_0-9]+)*')
    acceptorPersons: conlist(PersonWithAttainmentAcceptorType, min_length=1)
    organisations: conset(OrganisationRoleShareBase, min_length=1)
    state: Literal['ATTAINED', 'INCLUDED', 'SUBSTITUTED', 'FAILED']
    misregistration: bool
    misregistrationRationale: str | None = None
    primary: bool
    credits: float
    studyWeeks: str | None = None
    gradeScaleId: str
    gradeId: int
    gradeAverage: GradeAverage | None = None
    additionalInfo: LocalizedString | None = None
    administrativeNote: constr(min_length=1, max_length=SIS_MAX_MEDIUM_STRING_LENGTH) | None = None
    studyFieldUrn: constr(pattern='(urn:code:study-field)(:[A-z_0-9]+)*') | None = None
    workflowId: str | None = None
    moduleContentApplicationId: str | None = None
    creditTransferInfo: CreditTransferInfo | None = None
    cooperationNetworkStatus: dict | None = None  # CooperationNetworkStatus
    rdiCredits: float | None = None
    collaborationInstitution: dict | None = None  # CollaborationInstitution
    enrolmentRightId: str | None = None
    type: Literal[
        'AssessmentItemAttainment',
        'CourseUnitAttainment',
        'CustomCourseUnitAttainment',
        'ModuleAttainment',
        'CustomModuleAttainment',
        'DegreeProgrammeAttainment'
    ]
    attainmentDate: datetime.date

    @field_serializer('organisations')
    def organisations_as_list(self, val: set[OrganisationRoleShareBase], _info):
        return list(val)

    @field_serializer('attainmentDate')
    def date_as_isoformat(self, val: datetime.date, _info):
        return val.isoformat()

    @field_validator('attainmentDate')
    def attainment_date_valid(cls, val: datetime.date, _info):
        if val > datetime.date.today():
            raise ValueError("Attainment date must not be in the future")

        return val

    @model_validator(mode='after')
    def valid_primary_attainment(self):
        if self.documentState == 'DELETED' or not self.primary:
            return self

        if self.misregistration or self.state == 'FAILED':
            raise ValueError("Primary attainment cannot be misregistration or failed")

        return self

    @model_validator(mode='after')
    def valid_credit_transfer_info(self):
        if self.state == 'ATTAINED' and self.creditTransferInfo:
            raise ValueError("Attained attainment cannot have CreditTransferInfo")
        if self.state == 'SUBSTITUTED' and not self.creditTransferInfo:
            raise ValueError("Substituted attainment should have CreditTransferInfo")
        return self

    @field_validator("organisations")
    def has_valid_set_of_organisation_shares(cls, val: list[OrganisationRoleShareBase], _info):
        orgs_by_role_urn = group_by(
            val, lambda x: x.roleUrn
        )
        for urn, orgs in orgs_by_role_urn.items():
            if sum(_org.share for _org in orgs) != 1:
                raise ValueError("Sum of shares must be 1 for each roleUrn")
        return val


def localized_string_with_at_least_one_value(val: LocalizedString):
    if not (val.en or val.fi or val.sv):
        raise ValueError("LocalizedStrings must have at least one value")

    return val


LocalizedStringWithRequiredOneValue = Annotated[LocalizedString, AfterValidator(localized_string_with_at_least_one_value)]


class CourseUnitAttainment(Attainment):
    type: Literal['CourseUnitAttainment'] = 'CourseUnitAttainment'
    courseUnitId: str
    courseUnitGroupId: str
    evaluationCriteria: LocalizedString | None = None
    assessmentItemAttainmentIds: list[str] | None = None


class CustomCourseUnitAttainment(Attainment):
    type: Literal['CustomCourseUnitAttainment'] = 'CustomCourseUnitAttainment'
    name: LocalizedStringWithRequiredOneValue
    studyLevelUrn: constr(pattern='(urn:code:study-level)(:[A-z_0-9]+)*')
    courseUnitTypeUrn: constr(pattern='(urn:code:course-unit-type)(:[A-z_0-9]+)*')
    code: str
    customStudyDraftId: str | None = None


class CustomModuleAttainment(Attainment):
    type: Literal['CustomModuleAttainment'] = 'CustomModuleAttainment'
    code: str
    name: LocalizedStringWithRequiredOneValue
    nodes: list[AttainmentNode] | None = None


class DegreeProgrammeAttainment(Attainment):
    type: Literal['DegreeProgrammeAttainment'] = 'DegreeProgrammeAttainment'
    moduleId: str
    moduleGroupId: str
    nodes: list[AttainmentNode] | None = None
    embeddedModules: list[dict] | None = None
    acceptorPersons: list[PersonWithAttainmentAcceptorType] = Field(default_factory=lambda x: [])
    acceptorOrganisationIds: conlist(str, min_length=1, max_length=SIS_MAX_MEDIUM_SET_SIZE)
    educationClassificationUrn: constr(pattern='(urn:code:education-classification)(:[A-z_0-9]+)*')
    secondaryEducationClassificationUrn: constr(pattern='(urn:code:education-classification)(:[A-z_0-9]+)*') | None = None
    degreeTitleUrn: constr(pattern='(urn:code:degree-title)(:[A-z_0-9]+)*')
    honoraryTitleUrn: constr(pattern='(urn:code:honorary-title)(:[A-z_0-9]+)*') | None = None
    internationalContractualDegree: dict | None = None
