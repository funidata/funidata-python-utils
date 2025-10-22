from typing import Literal, Annotated

from pydantic import conlist, Field, BaseModel

from funidata_utils.schemas.sisu.base import SisBase
from funidata_utils.schemas.sisu.common import (
    OTM_ID_REGEX_VALIDATED_STR, SIS_MAX_SMALL_SET_SIZE, LocalizedString, LocalDateRange, sis_code_urn_pattern,
    STRIPPED_STR, OrganisationRoleShare, SIS_MAX_MEDIUM_SET_SIZE
)


class EducationChildOption(BaseModel):
    localId: str
    moduleGroupId: OTM_ID_REGEX_VALIDATED_STR
    acceptanceType: Literal['AUTOMATIC', 'ACCEPTED_BY_TEACHER']
    degreeTitleUrn: Annotated[STRIPPED_STR | None, Field(pattern=sis_code_urn_pattern('degree-title'))] = None
    educationClassificationUrn: Annotated[STRIPPED_STR | None, Field(pattern=sis_code_urn_pattern('education-classification'))] = None


class EducationOption(BaseModel):
    localId: str
    moduleGroupId: OTM_ID_REGEX_VALIDATED_STR
    childOptions: conlist(EducationChildOption, min_length=0, max_length=SIS_MAX_MEDIUM_SET_SIZE)
    acceptanceType: Literal['AUTOMATIC', 'ACCEPTED_BY_TEACHER']
    childNaming: Annotated[STRIPPED_STR, Field(pattern=sis_code_urn_pattern('education-option-naming-type'))]
    degreeTitleUrn: Annotated[STRIPPED_STR | None, Field(pattern=sis_code_urn_pattern('degree-title'))] = None
    educationClassificationUrn: Annotated[STRIPPED_STR | None, Field(pattern=sis_code_urn_pattern('education-classification'))] = None


class EducationPhase(BaseModel):
    name: LocalizedString
    options: conlist(EducationOption, max_length=SIS_MAX_MEDIUM_SET_SIZE, min_length=1)


class LearningOpportunitySelectionPath(BaseModel):
    educationPhase1GroupId: OTM_ID_REGEX_VALIDATED_STR | None = None
    educationPhase1ChildGroupId: OTM_ID_REGEX_VALIDATED_STR | None = None
    educationPhase2GroupId: OTM_ID_REGEX_VALIDATED_STR | None = None
    educationPhase2ChildGroupId: OTM_ID_REGEX_VALIDATED_STR | None = None

# structure.learningOpportunities.0.allowedPaths.0.educationPhase2ChildGroupId

class LearningOpportunity(BaseModel):
    localId: str
    name: LocalizedString
    allowedPaths: conlist(LearningOpportunitySelectionPath, min_length=0, max_length=SIS_MAX_MEDIUM_SET_SIZE)
    admissionTargetIds: conlist(OTM_ID_REGEX_VALIDATED_STR, min_length=0, max_length=SIS_MAX_MEDIUM_SET_SIZE)
    phase1EducationClassificationUrn: Annotated[STRIPPED_STR | None, Field(pattern=sis_code_urn_pattern('education-classification'))] = None
    phase2EducationClassificationUrn: Annotated[STRIPPED_STR | None, Field(pattern=sis_code_urn_pattern('education-classification'))] = None


class EducationStructure(BaseModel):
    phase1: EducationPhase
    phase2: EducationPhase | None = None
    learningOpportunities: conlist(LearningOpportunity, max_length=SIS_MAX_SMALL_SET_SIZE, min_length=1)


class PersonWithEducationResponsibilityInfoType(BaseModel):
    text: LocalizedString | None = None
    personId: OTM_ID_REGEX_VALIDATED_STR | None = None
    roleUrn: Literal[
        'urn:code:education-responsibility-info-type:academic-responsibility',
        'urn:code:education-responsibility-info-type:administrative-person',
        'urn:code:education-responsibility-info-type:contact-info'
    ]
    validity: LocalDateRange | None = None
    validityPeriod: LocalDateRange | None = None


class Education(SisBase):
    documentState: Literal['ACTIVE', 'DRAFT', 'DELETED']
    id: OTM_ID_REGEX_VALIDATED_STR
    universityOrgIds: conlist(OTM_ID_REGEX_VALIDATED_STR, max_length=SIS_MAX_SMALL_SET_SIZE)
    groupId: OTM_ID_REGEX_VALIDATED_STR
    name: LocalizedString
    validityPeriod: LocalDateRange
    code: str
    educationType: Annotated[STRIPPED_STR, Field(pattern=sis_code_urn_pattern('education-type'))]
    specialisationStudiesClassificationUrn: Annotated[str | None, Field(pattern=sis_code_urn_pattern('specialisation-studies-classification'))] = None
    studyFields: conlist(Annotated[str, Field(pattern=sis_code_urn_pattern('study-field'))], max_length=SIS_MAX_SMALL_SET_SIZE, min_length=1)
    organisations: conlist(OrganisationRoleShare, max_length=SIS_MAX_MEDIUM_SET_SIZE, min_length=1)
    attainmentLanguages: conlist(
        Annotated[STRIPPED_STR, Field(pattern=sis_code_urn_pattern('language'))],
        max_length=SIS_MAX_MEDIUM_SET_SIZE
    ) | None = None
    educationLocationUrn: Annotated[STRIPPED_STR | None, Field(pattern=sis_code_urn_pattern('municipality'))] = None
    outcomes: LocalizedString | None = None
    responsibilityInfos: conlist(PersonWithEducationResponsibilityInfoType, min_length=1, max_length=SIS_MAX_MEDIUM_SET_SIZE)
    structure: EducationStructure
    defaultStudyRightExpirationRulesUrn: Annotated[STRIPPED_STR, Field(pattern=sis_code_urn_pattern('study-right-expiration-rules'))]
    defaultDecreeOnUniversityDegreesUrn: Annotated[STRIPPED_STR, Field(pattern=sis_code_urn_pattern('decree-on-university-degrees'))]
    studyRightExtensionInstructions: LocalizedString | None = None
    studySelectionRequirement: Literal['UNRESTRICTED', 'SELECTION_REQUIRED', 'ENROLMENT_RIGHT_REQUIRED']
    fundingSourceEducationUrn: Annotated[STRIPPED_STR | None, Field(pattern=sis_code_urn_pattern('funding-source-education'))] = None
    isMultiformEducation: bool
    type: Literal['Education']
