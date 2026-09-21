import copy

import pytest

from funidata_utils.data_scramblers.ilmo_enrolment import IlmoEnrolmentScrambler


@pytest.mark.unit
def test_enrolment_scrambler_scrambles_keys():
    data = {
        "documentState": "DRAFT",
        "id": "otm-123456",
        "personId": "otm-123456",
        "courseUnitRealisationId": "otm-123456",
        "courseUnitId": "otm-123456",
        "assessmentItemId": "otm-123456",
        "studyRightId": "otm-123456",
        "openUniversityCartId": "otm-123456",
        "openUniversityCartItemId": "otm-123456",
        "state": "NOT_ENROLLED",
        "processingState": "NOT_PROCESSED",
        "studySubGroups": [
            {
                "studySubGroupId": "otm-123456",
                "enrolmentStudySubGroupPriority": "PRIMARY",
                "isInCalendar": True
            }
        ],
        "studyGroupSets": [
            {
                "studyGroupSetId": "otm-123456",
                "targetStudySubGroupAmount": 0
            }
        ],
        "confirmedStudySubGroupIds": [
            "otm-123456"
        ],
        "tentativeStudySubGroupIds": [
            "otm-123456"
        ],
        "enrolmentDateTime": "2026-09-21T07:45:37.841Z",
        "isInCalendar": True,
        "colorIndex": 0,
        "quotaIds": [
            "otm-123456"
        ],
        "activeQuotaId": "otm-123456",
        "allocatedQuotaId": "otm-123456",
        "maximumQuotaIds": [
            "otm-123456"
        ],
        "enrolmentRightId": "otm-123456",
        "replacedByEnrolmentId": "otm-123456",
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
            "selectionItemStatusInfo": "string"
        },
        "studentConsentForOutboundDataTransfer": {
            "consentApprovalType": "APPROVED",
            "consentTargetType": "CROSS_STUDY_DATA_TRANSFER_ON_OUTBOUND_ENROLMENT",
            "clause": "string"
        }
    }

    scrambled_data = IlmoEnrolmentScrambler.scramble(copy.deepcopy(data), set())

    assert len(IlmoEnrolmentScrambler.dict_items_with_scrambling()) >= 2
    for key, _ in IlmoEnrolmentScrambler.dict_items_with_scrambling():
        if isinstance(scrambled_data.get(key), bool):
            # Cannot reliably test for bool 50/50 changes
            continue

        assert scrambled_data.get(key, -42) != data.get(key, -42)


@pytest.mark.unit
def test_enrolment_scrambler_handles_lists_correctly():
    data = {
        "documentState": "DRAFT",
        "id": "otm-123456",
        "personId": "otm-123456",
        "courseUnitRealisationId": "otm-123456",
        "courseUnitId": "otm-123456",
        "assessmentItemId": "otm-123456",
        "studyRightId": "otm-123456",
        "openUniversityCartId": "otm-123456",
        "openUniversityCartItemId": "otm-123456",
        "state": "NOT_ENROLLED",
        "processingState": "NOT_PROCESSED",
        "studySubGroups": [
            {
                "studySubGroupId": "otm-123456",
                "enrolmentStudySubGroupPriority": "PRIMARY",
                "isInCalendar": True
            }
        ],
        "studyGroupSets": [
            {
                "studyGroupSetId": "otm-123456",
                "targetStudySubGroupAmount": 0
            }
        ],
        "confirmedStudySubGroupIds": [
            "otm-123456"
        ],
        "tentativeStudySubGroupIds": [
            "otm-123456"
        ],
        "enrolmentDateTime": "2026-09-21T07:45:37.841Z",
        "isInCalendar": True,
        "colorIndex": 0,
        "quotaIds": [
            "otm-123456"
        ],
        "activeQuotaId": "otm-123456",
        "allocatedQuotaId": "otm-123456",
        "maximumQuotaIds": [
            "otm-123456"
        ],
        "enrolmentRightId": "otm-123456",
        "replacedByEnrolmentId": "otm-123456",
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
            "selectionItemStatusInfo": "string"
        },
        "studentConsentForOutboundDataTransfer": {
            "consentApprovalType": "APPROVED",
            "consentTargetType": "CROSS_STUDY_DATA_TRANSFER_ON_OUTBOUND_ENROLMENT",
            "clause": "string"
        }
    }

    scrambled_data = IlmoEnrolmentScrambler.scramble(copy.deepcopy(data), set())
    list_keys = {
        'maximumQuotaIds', 'quotaIds',
        'tentativeStudySubGroupIds', 'confirmedStudySubGroupIds',
        'studyGroupSets', 'studySubGroups',
    }
    for key in list_keys:
        assert isinstance(scrambled_data[key], list), scrambled_data[key]
