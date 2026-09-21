import copy

import pytest

from funidata_utils.data_scramblers.thesis import ThesisScrambler
from funidata_utils.schemas.sisu import Thesis


@pytest.mark.unit
def test_thesis_scrambler_scrambles():
    data = {
        "documentState": "ACTIVE",
        "id": "otm-123456",
        "personId": "otm-123456",
        "attainmentId": "otm-123456",
        "title": {
          "fi": "Finnish version",
          "sv": "Swedish version",
          "en": "English version"
        },
        "subject": {
          "fi": "Finnish version",
          "sv": "Swedish version",
          "en": "English version"
        },
        "thesisTypeUrn": "urn:code:thesis-type:amk-bachelors-thesis",
        "responsibilityInfos": [
          {
            "text": {
              "fi": "Finnish version",
              "sv": "Swedish version",
              "en": "English version"
            },
            "personId": "otm-123456",
            "roleUrn": "urn:code:attainment-acceptor-type:approved-by",
            "title": {
              "fi": "Finnish version",
              "sv": "Swedish version",
              "en": "English version"
            }
          }
        ],
        "organisations": [
          {
            "organisationId": "otm-123456",
            "educationalInstitutionUrn": "urn:code:educational-institution:01",
            "roleUrn": "urn:code:organisation-role:responsible-organisation",
            "share": 1
          }
        ],
        "courseUnitId": "otm-123456",
        "courseUnitGroupId": "otm-123456",
        "state": "ATTAINED",
        "publicInspectionDate": "2026-09-21",
        "commissionType": "NONE"
    }

    scrambled_data = ThesisScrambler.scramble(copy.deepcopy(data), set())

    assert len(ThesisScrambler.dict_items_with_scrambling()) >= 3
    for key, _ in ThesisScrambler.dict_items_with_scrambling():
        if isinstance(scrambled_data.get(key), bool):
            # Cannot reliably test for bool 50/50 changes
            continue

        assert scrambled_data.get(key, -42) != data.get(key, -42)

    # TODO: Update when real responsibility info scrambling is implemented
    # Thesis.model_validate(scrambled_data)