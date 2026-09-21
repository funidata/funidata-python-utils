import copy

import pytest

from funidata_utils.data_scramblers.attained_qualification import AttainedQualificationScrambler
from funidata_utils.schemas.sisu import AttainedQualification


@pytest.mark.unit
def test_attained_qualification_scrambler_scrambles_keys():
    data = {
        "documentState": "DRAFT",
        "id": "otm-123456",
        "qualificationId": "otm-123456",
        "personId": "otm-123456",
        "studyRightId": "otm-123456",
        "moduleGroupId": "otm-123456",
        "additionalInformation": "string",
        "associatedStudies": [
            {
                "description": "string",
                "credits": 0,
                "attainmentLocation": "urn:code:educational-institution:*",
                "associatedDegree": "string",
                "attainmentDate": "2026-09-18"
            }
        ],
        "attainmentDate": "2026-09-18",
        "studyFieldUrn": "urn:code:study-field:*",
        "attainmentMethod": "AUTOMATIC",
        "credits": 0,
        "attainmentIds": [
            "otm-123456"
        ],
        "childAttainedQualificationIds": [
            "otm-123456"
        ],
        "registrationDate": "2026-09-18",
        "verifierPersonId": "otm-123456"
    }

    scrambled_data = AttainedQualificationScrambler.scramble(copy.deepcopy(data), set())

    assert len(AttainedQualificationScrambler.dict_items_with_scrambling()) >= 2
    for key, _ in AttainedQualificationScrambler.dict_items_with_scrambling():
        if isinstance(scrambled_data.get(key), bool):
            # Cannot reliably test for bool 50/50 changes
            continue

        assert scrambled_data.get(key, -42) != data.get(key, -42)

    AttainedQualification.model_validate(scrambled_data)


@pytest.mark.unit
def test_attained_qualification_scrambler_handles_lists_correctly():
    data = {
        "documentState": "DRAFT",
        "id": "otm-123456",
        "qualificationId": "otm-123456",
        "personId": "otm-123456",
        "studyRightId": "otm-123456",
        "moduleGroupId": "otm-123456",
        "additionalInformation": "string",
        "associatedStudies": [
            {
                "description": "string",
                "credits": 0,
                "attainmentLocation": "urn:code:educational-institution:*",
                "associatedDegree": "string",
                "attainmentDate": "2026-09-18"
            }
        ],
        "attainmentDate": "2026-09-18",
        "studyFieldUrn": "urn:code:study-field:*",
        "attainmentMethod": "AUTOMATIC",
        "credits": 0,
        "attainmentIds": [
            "otm-123456"
        ],
        "childAttainedQualificationIds": [
            "otm-123456"
        ],
        "registrationDate": "2026-09-18",
        "verifierPersonId": "otm-123456"
    }

    scrambled_data = AttainedQualificationScrambler.scramble(copy.deepcopy(data), set())
    list_keys = {'associatedStudies', 'attainmentIds', 'childAttainedQualificationIds'}
    for key in list_keys:
        assert isinstance(scrambled_data[key], list), scrambled_data[key]

    AttainedQualification.model_validate(scrambled_data)
