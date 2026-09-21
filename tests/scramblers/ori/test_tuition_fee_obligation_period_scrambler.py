import copy

import pytest

from funidata_utils.data_scramblers.tuition_fee_obligation_period import TuitionFeeObligationPeriodScrambler


@pytest.mark.unit
def test_tuition_fee_scrambler_scrambles_additional_info():
    data = {
        "id": "otm-123456",
        "studyRightId": "otm-123456",
        "valid": {
            "startDate": "2026-09-21",
            "endDate": "2026-09-21"
        },
        "tuitionFee": 0,
        "exempt": True,
        "additionalInfo": {
            "fi": "Finnish version",
            "sv": "Swedish version",
            "en": "English version"
        }
    }

    scrambled_data = TuitionFeeObligationPeriodScrambler.scramble(copy.deepcopy(data), set())

    assert len(TuitionFeeObligationPeriodScrambler.dict_items_with_scrambling()) >= 1
    for key, _ in TuitionFeeObligationPeriodScrambler.dict_items_with_scrambling():
        if isinstance(scrambled_data.get(key), bool):
            # Cannot reliably test for bool 50/50 changes
            continue

        assert scrambled_data.get(key, -42) != data.get(key, -42)