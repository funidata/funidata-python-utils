import copy

import pytest

from funidata_utils.data_scramblers.study_right import StudyRightScrambler
from funidata_utils.schemas.sisu import StudyRight


@pytest.mark.unit
def test_study_right_scrambler_scrambles_keys():
    data = {
        "documentState": "DRAFT",
        "id": "otm-123456",
        "snapshotDateTime": "2026-09-21T07:57:56.057Z",
        "studentId": "otm-123456",
        "educationId": "otm-123456",
        "organisationId": "otm-123456",
        "learningOpportunityId": "otm-123456",
        "admissionTargetId": "otm-123456",
        "admissionIdentifier": "string",
        "decreeOnUniversityDegreesUrn": "urn:code:decree-on-university-degrees:123",
        "studyRightExpirationRulesUrn": "urn:code:study-right-expiration-rules:123",
        "degreeRegulations": "string",
        "valid": {
            "startDate": "2026-09-21",
            "endDate": "2026-09-21"
        },
        "grantDate": "2026-09-21",
        "studyStartDate": "2026-09-21",
        "alternativeStudyStartDate": "2026-09-21",
        "transferOutDate": "2026-09-21",
        "transferOutUniversityUrn": "urn:code:educational-institution:123",
        "homeOrganisationUrn": "urn:code:educational-institution:123",
        "termRegistrations": [
            {
                "localId": "otm-123456",
                "studyTerm": {
                    "studyYearStartYear": 0,
                    "termIndex": 0
                },
                "registrationDate": "2026-09-21",
                "termRegistrationType": "ATTENDING",
                "previousRegistrationType": "ATTENDING",
                "previousRegistrationDate": "2026-09-21",
                "statutoryAbsence": True,
                "statutoryAbsenceDate": "2026-09-21",
                "statutoryAbsenceChangedBy": "otm-123456",
                "tuitionFeePaymentState": "PAID"
            }
        ],
        "studyRightExtensions": [
            {
                "localId": "otm-123456",
                "state": "ACTIVE",
                "extensionCount": 1,
                "extensionStartDate": "2026-09-21",
                "grantDate": "2026-09-21",
                "workflowId": "otm-123456",
                "grantReason": "string",
                "grantedBy": "otm-123456",
                "deleteDate": "2026-09-21",
                "deleteReason": "string",
                "deletedBy": "otm-123456"
            }
        ],
        "studyRightCancellation": {
            "cancellationDate": "2020-09-21",
            "cancellationReason": "string",
            "cancellationType": "RESCINDED"
        },
        "studyRightPassivations": [
            {
                "localId": "otm-123456",
                "passivationType": "DEGREE_REGULATIONS",
                "valid": {
                    "startDate": "2026-09-21",
                    "endDate": "2026-09-21"
                },
                "additionalInfo": "string"
            }
        ],
        "studyRightGraduation": {
            "phase1GraduationDate": "2026-09-21",
            "phase2GraduationDate": "2026-09-21"
        },
        "acceptedSelectionPath": {
            "educationPhase1GroupId": "otm-123456",
            "educationPhase1ChildGroupId": "otm-123456",
            "educationPhase2GroupId": "otm-123456",
            "educationPhase2ChildGroupId": "otm-123456"
        },
        "requestedSelectionPath": {
            "educationPhase1GroupId": "otm-123456",
            "educationPhase1ChildGroupId": "otm-123456",
            "educationPhase2GroupId": "otm-123456",
            "educationPhase2ChildGroupId": "otm-123456"
        },
        "studyRightTransfer": {
            "originalStartDate": "2026-09-21",
            "originalUniversityUrn": "urn:code:educational-institution:123",
            "usedTerms": 0,
            "usedAbsenceTerms": 0,
            "usedStatutoryAbsenceTerms": 0,
            "transferComments": "string"
        },
        "phase1MinorSelections": [
            {
                "localId": "otm-123456",
                "validityPeriod": {
                    "startDate": "2026-09-21",
                    "endDate": "2026-09-21"
                },
                "acceptorPersonId": "otm-123456",
                "acceptanceDate": "2026-09-21",
                "moduleGroupId": "otm-123456",
                "selectionState": "REQUESTED",
                "selectionType": "urn:code:study-right-selection-type:minor-study-right"
            }
        ],
        "phase2MinorSelections": [
            {
                "localId": "otm-123456",
                "validityPeriod": {
                    "startDate": "2026-09-21",
                    "endDate": "2026-09-21"
                },
                "acceptorPersonId": "otm-123456",
                "acceptanceDate": "2026-09-21",
                "moduleGroupId": "otm-123456",
                "selectionState": "REQUESTED",
                "selectionType": "urn:code:study-right-selection-type:minor-study-right"
            }
        ],
        "state": "NOT_STARTED",
        "statePeriods": [
            {
                "state": "NOT_STARTED",
                "startDate": "2026-09-21",
                "endDate": "2026-09-21"
            }
        ],
        "personalizedSelectionPath": {
            "phase1": {
                "rationale": "string",
                "createdBy": "otm-123456",
                "createdOn": "2026-09-21T07:57:56.058Z",
                "moduleGroupId": "otm-123456",
                "childModuleGroupId": "otm-123456",
                "childNamingUrn": "urn:code:education-option-naming-type:123",
                "degreeTitleUrn": "urn:code:degree-title:123",
                "educationClassificationUrn": "urn:code:education-classification:123"
            },
            "phase2": {
                "rationale": "string",
                "createdBy": "otm-123456",
                "createdOn": "2026-09-21T07:57:56.058Z",
                "moduleGroupId": "otm-123456",
                "childModuleGroupId": "otm-123456",
                "childNamingUrn": "urn:code:education-option-naming-type:123",
                "degreeTitleUrn": "urn:code:degree-title:123",
                "educationClassificationUrn": "urn:code:education-classification:123"
            }
        },
        "courseUnitSelections": [
            {
                "localId": "otm-123456",
                "validityPeriod": {
                    "startDate": "2026-09-21",
                    "endDate": "2026-09-21"
                },
                "acceptorPersonId": "otm-123456",
                "acceptanceDate": "2026-09-21",
                "courseUnitGroupId": "otm-123456"
            }
        ],
        "moduleSelections": [
            {
                "localId": "otm-123456",
                "validityPeriod": {
                    "startDate": "2026-09-21",
                    "endDate": "2026-09-21"
                },
                "acceptorPersonId": "otm-123456",
                "acceptanceDate": "2026-09-21",
                "moduleGroupId": "otm-123456"
            }
        ],
        "studyFieldUrn": "urn:code:study-field:123",
        "phase1EducationClassificationUrn": "urn:code:education-classification:123",
        "phase2EducationClassificationUrn": "urn:code:education-classification:123",
        "phase1EducationClassificationLocked": True,
        "phase2EducationClassificationLocked": True,
        "fundingSourceUrn": "urn:code:funding-source:123",
        "phase1QualificationUrns": [
            "string"
        ],
        "phase2QualificationUrns": [
            "string"
        ],
        "phase1EducationLocationUrn": "urn:code:municipality:123",
        "phase2EducationLocationUrn": "urn:code:municipality:123",
        "phase1InternationalContractualDegree": {
            "localId": "otm-123456",
            "internationalContractualDegreeAgreementId": "otm-123456",
            "attainableDegrees": [
                {
                    "degreeName": "string",
                    "internationalInstitutionUrn": "urn:code:international-institution:123"
                }
            ]
        },
        "phase2InternationalContractualDegree": {
            "localId": "otm-123456",
            "internationalContractualDegreeAgreementId": "otm-123456",
            "attainableDegrees": [
                {
                    "degreeName": "string",
                    "internationalInstitutionUrn": "urn:code:international-institution:123"
                }
            ]
        },
        "admissionTypeUrn": "urn:code:admission-type:123",
        "codeUrns": [
            "urn:code:code"
        ],
        "additionalInformation": {
            "fi": "Finnish version",
            "sv": "Swedish version",
            "en": "English version"
        },
        "cooperationNetworkRights": [
            {
                "localId": "otm-123456",
                "cooperationNetworkId": "otm-123456",
                "validityPeriod": {
                    "startDate": "2026-09-21",
                    "endDate": "2026-09-21"
                },
                "updateType": "MANUAL",
                "targetGroupUpdateDate": "2026-09-21"
            }
        ],
        "cooperationNetworkStatus": {
            "direction": "INBOUND",
            "organisationTkCode": "string",
            "outboundStatus": "NOT_VALID",
            "rejectionReason": {
                "fi": "Finnish version",
                "sv": "Swedish version",
                "en": "English version"
            },
            "outboundStatusMessage": "string",
            "cooperationNetworkId": "otm-123456",
            "universityOrgId": "otm-123456",
            "homeStudyRightId": "string",
            "inboundStatus": "ACCEPTED",
            "homeStudyRightValidity": {
                "startDate": "2026-09-21",
                "endDate": "2026-09-21"
            }
        },
        "schoolEducationLanguageUrn": "urn:code:school-education-language:123"
    }
    scrambled_data = StudyRightScrambler.scramble(copy.deepcopy(data), set())

    assert len(StudyRightScrambler.dict_items_with_scrambling()) >= 2
    for key, _ in StudyRightScrambler.dict_items_with_scrambling():
        if isinstance(scrambled_data.get(key), bool):
            # Cannot reliably test for bool 50/50 changes
            continue

        assert scrambled_data.get(key, -42) != data.get(key, -42)

    StudyRight.model_validate(scrambled_data)


@pytest.mark.unit
def test_study_right_scrambler_handles_lists_correctly():
    data = {
        "documentState": "DRAFT",
        "id": "otm-123456",
        "snapshotDateTime": "2026-09-21T07:57:56.057Z",
        "studentId": "otm-123456",
        "educationId": "otm-123456",
        "organisationId": "otm-123456",
        "learningOpportunityId": "otm-123456",
        "admissionTargetId": "otm-123456",
        "admissionIdentifier": "string",
        "decreeOnUniversityDegreesUrn": "urn:code:decree-on-university-degrees:123",
        "studyRightExpirationRulesUrn": "urn:code:study-right-expiration-rules:123",
        "degreeRegulations": "string",
        "valid": {
            "startDate": "2026-09-21",
            "endDate": "2026-09-21"
        },
        "grantDate": "2026-09-21",
        "studyStartDate": "2026-09-21",
        "alternativeStudyStartDate": "2026-09-21",
        "transferOutDate": "2026-09-21",
        "transferOutUniversityUrn": "urn:code:educational-institution:123",
        "homeOrganisationUrn": "urn:code:educational-institution:123",
        "termRegistrations": [
            {
                "localId": "otm-123456",
                "studyTerm": {
                    "studyYearStartYear": 0,
                    "termIndex": 0
                },
                "registrationDate": "2026-09-21",
                "termRegistrationType": "ATTENDING",
                "previousRegistrationType": "ATTENDING",
                "previousRegistrationDate": "2026-09-21",
                "statutoryAbsence": True,
                "statutoryAbsenceDate": "2026-09-21",
                "statutoryAbsenceChangedBy": "otm-123456",
                "tuitionFeePaymentState": "PAID"
            }
        ],
        "studyRightExtensions": [
            {
                "localId": "otm-123456",
                "state": "ACTIVE",
                "extensionCount": 1,
                "extensionStartDate": "2026-09-21",
                "grantDate": "2026-09-21",
                "workflowId": "otm-123456",
                "grantReason": "string",
                "grantedBy": "otm-123456",
                "deleteDate": "2026-09-21",
                "deleteReason": "string",
                "deletedBy": "otm-123456"
            }
        ],
        "studyRightCancellation": {
            "cancellationDate": "2020-09-21",
            "cancellationReason": "string",
            "cancellationType": "RESCINDED"
        },
        "studyRightPassivations": [
            {
                "localId": "otm-123456",
                "passivationType": "DEGREE_REGULATIONS",
                "valid": {
                    "startDate": "2026-09-21",
                    "endDate": "2026-09-21"
                },
                "additionalInfo": "string"
            }
        ],
        "studyRightGraduation": {
            "phase1GraduationDate": "2026-09-21",
            "phase2GraduationDate": "2026-09-21"
        },
        "acceptedSelectionPath": {
            "educationPhase1GroupId": "otm-123456",
            "educationPhase1ChildGroupId": "otm-123456",
            "educationPhase2GroupId": "otm-123456",
            "educationPhase2ChildGroupId": "otm-123456"
        },
        "requestedSelectionPath": {
            "educationPhase1GroupId": "otm-123456",
            "educationPhase1ChildGroupId": "otm-123456",
            "educationPhase2GroupId": "otm-123456",
            "educationPhase2ChildGroupId": "otm-123456"
        },
        "studyRightTransfer": {
            "originalStartDate": "2026-09-21",
            "originalUniversityUrn": "urn:code:educational-institution:123",
            "usedTerms": 0,
            "usedAbsenceTerms": 0,
            "usedStatutoryAbsenceTerms": 0,
            "transferComments": "string"
        },
        "phase1MinorSelections": [
            {
                "localId": "otm-123456",
                "validityPeriod": {
                    "startDate": "2026-09-21",
                    "endDate": "2026-09-21"
                },
                "acceptorPersonId": "otm-123456",
                "acceptanceDate": "2026-09-21",
                "moduleGroupId": "otm-123456",
                "selectionState": "REQUESTED",
                "selectionType": "urn:code:study-right-selection-type:minor-study-right"
            }
        ],
        "phase2MinorSelections": [
            {
                "localId": "otm-123456",
                "validityPeriod": {
                    "startDate": "2026-09-21",
                    "endDate": "2026-09-21"
                },
                "acceptorPersonId": "otm-123456",
                "acceptanceDate": "2026-09-21",
                "moduleGroupId": "otm-123456",
                "selectionState": "REQUESTED",
                "selectionType": "urn:code:study-right-selection-type:minor-study-right"
            }
        ],
        "state": "NOT_STARTED",
        "statePeriods": [
            {
                "state": "NOT_STARTED",
                "startDate": "2026-09-21",
                "endDate": "2026-09-21"
            }
        ],
        "personalizedSelectionPath": {
            "phase1": {
                "rationale": "string",
                "createdBy": "otm-123456",
                "createdOn": "2026-09-21T07:57:56.058Z",
                "moduleGroupId": "otm-123456",
                "childModuleGroupId": "otm-123456",
                "childNamingUrn": "urn:code:education-option-naming-type:123",
                "degreeTitleUrn": "urn:code:degree-title:123",
                "educationClassificationUrn": "urn:code:education-classification:123"
            },
            "phase2": {
                "rationale": "string",
                "createdBy": "otm-123456",
                "createdOn": "2026-09-21T07:57:56.058Z",
                "moduleGroupId": "otm-123456",
                "childModuleGroupId": "otm-123456",
                "childNamingUrn": "urn:code:education-option-naming-type:123",
                "degreeTitleUrn": "urn:code:degree-title:123",
                "educationClassificationUrn": "urn:code:education-classification:123"
            }
        },
        "courseUnitSelections": [
            {
                "localId": "otm-123456",
                "validityPeriod": {
                    "startDate": "2026-09-21",
                    "endDate": "2026-09-21"
                },
                "acceptorPersonId": "otm-123456",
                "acceptanceDate": "2026-09-21",
                "courseUnitGroupId": "otm-123456"
            }
        ],
        "moduleSelections": [
            {
                "localId": "otm-123456",
                "validityPeriod": {
                    "startDate": "2026-09-21",
                    "endDate": "2026-09-21"
                },
                "acceptorPersonId": "otm-123456",
                "acceptanceDate": "2026-09-21",
                "moduleGroupId": "otm-123456"
            }
        ],
        "studyFieldUrn": "urn:code:study-field:123",
        "phase1EducationClassificationUrn": "urn:code:education-classification:123",
        "phase2EducationClassificationUrn": "urn:code:education-classification:123",
        "phase1EducationClassificationLocked": True,
        "phase2EducationClassificationLocked": True,
        "fundingSourceUrn": "urn:code:funding-source:123",
        "phase1QualificationUrns": [
            "string"
        ],
        "phase2QualificationUrns": [
            "string"
        ],
        "phase1EducationLocationUrn": "urn:code:municipality:123",
        "phase2EducationLocationUrn": "urn:code:municipality:123",
        "phase1InternationalContractualDegree": {
            "localId": "otm-123456",
            "internationalContractualDegreeAgreementId": "otm-123456",
            "attainableDegrees": [
                {
                    "degreeName": "string",
                    "internationalInstitutionUrn": "urn:code:international-institution:123"
                }
            ]
        },
        "phase2InternationalContractualDegree": {
            "localId": "otm-123456",
            "internationalContractualDegreeAgreementId": "otm-123456",
            "attainableDegrees": [
                {
                    "degreeName": "string",
                    "internationalInstitutionUrn": "urn:code:international-institution:123"
                }
            ]
        },
        "admissionTypeUrn": "urn:code:admission-type:123",
        "codeUrns": [
            "urn:code:code"
        ],
        "additionalInformation": {
            "fi": "Finnish version",
            "sv": "Swedish version",
            "en": "English version"
        },
        "cooperationNetworkRights": [
            {
                "localId": "otm-123456",
                "cooperationNetworkId": "otm-123456",
                "validityPeriod": {
                    "startDate": "2026-09-21",
                    "endDate": "2026-09-21"
                },
                "updateType": "MANUAL",
                "targetGroupUpdateDate": "2026-09-21"
            }
        ],
        "cooperationNetworkStatus": {
            "direction": "INBOUND",
            "organisationTkCode": "string",
            "outboundStatus": "NOT_VALID",
            "rejectionReason": {
                "fi": "Finnish version",
                "sv": "Swedish version",
                "en": "English version"
            },
            "outboundStatusMessage": "string",
            "cooperationNetworkId": "otm-123456",
            "universityOrgId": "otm-123456",
            "homeStudyRightId": "string",
            "inboundStatus": "ACCEPTED",
            "homeStudyRightValidity": {
                "startDate": "2026-09-21",
                "endDate": "2026-09-21"
            }
        },
        "schoolEducationLanguageUrn": "urn:code:school-education-language:123"
    }
    scrambled_data = StudyRightScrambler.scramble(copy.deepcopy(data), set())
    list_keys = {
        'termRegistrations', 'studyRightExtensions', 'studyRightPassivations',
        'phase1MinorSelections', 'phase2MinorSelections', 'statePeriods',
        'courseUnitSelections', 'moduleSelections',
        'phase1QualificationUrns', 'phase2QualificationUrns',
        'codeUrns', 'cooperationNetworkRights'
    }
    for key in list_keys:
        if key in {'termRegistrations'}:
            # skip termregs since it's ... not a real part of studyrights.
            continue
        assert isinstance(scrambled_data[key], list), (key, scrambled_data[key], data[key])

    StudyRight.model_validate(scrambled_data)
