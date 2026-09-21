import copy

import pytest

from funidata_utils.data_scramblers.mobility_period import MobilityPeriodScrambler
from funidata_utils.schemas.sisu import MobilityPeriod


@pytest.mark.unit
def test_mobility_period_scrambler_scrambles_keys():
    data = {
        "documentState": "DRAFT",
        "id": "otm-123456",
        "studyRightId": "otm-123456",
        "personId": "otm-123456",
        "mobilityDirection": "INBOUND",
        "activityPeriod": {
            "startDate": "2026-09-18",
            "endDate": "2026-09-18"
        },
        "phase": "PHASE1",
        "mobilityProgramUrn": "urn:code:mobility-program:123",
        "mobilityProgramDescription": "string",
        "mobilityTypeUrn": "urn:code:mobility-type:123",
        "countryUrn": "urn:code:country:123",
        "internationalInstitutionUrn": "urn:code:international-institution:123",
        "organisation": "string",
        "mobilityStudyRightTypeUrn": "urn:code:mobility-study-right-type:123",
        "virtualMobilityType": "None",
        "isCancelled": True
    }
    scrambled_data = MobilityPeriodScrambler.scramble(copy.deepcopy(data), set())

    assert len(MobilityPeriodScrambler.dict_items_with_scrambling()) >= 2
    for key, _ in MobilityPeriodScrambler.dict_items_with_scrambling():
        if isinstance(scrambled_data.get(key), bool):
            # Cannot reliably test for bool 50/50 changes
            continue

        assert scrambled_data.get(key, -42) != data.get(key, -42)

    MobilityPeriod.model_validate(scrambled_data)
