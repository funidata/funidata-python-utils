import copy

import pytest

from funidata_utils.data_scramblers.kori_person import KoriPersonScrambler
from funidata_utils.schemas.sisu import PublicPerson


@pytest.mark.unit
def test_public_person_scrambler_scrambles_keys():
    data = {
        "documentState": "DRAFT",
        "id": "otm-123456",
        "universityOrgIds": [
            "otm-123456"
        ],
        "titles": [
            {
                "fi": "Finnish version",
                "sv": "Swedish version",
                "en": "English version"
            }
        ],
        "firstName": "string",
        "lastName": "string",
        "emailAddress": "string"
    }

    scrambled_data = KoriPersonScrambler.scramble(copy.deepcopy(data), set())

    assert scrambled_data['emailAddress'] != 'string'
    assert len(KoriPersonScrambler.dict_items_with_scrambling()) >= 4
    for key, _ in KoriPersonScrambler.dict_items_with_scrambling():
        if isinstance(scrambled_data.get(key), bool):
            # Cannot reliably test for bool 50/50 changes
            continue

        assert scrambled_data.get(key, -42) != data.get(key, -42)

    PublicPerson.model_validate(scrambled_data)


@pytest.mark.unit
def test_public_person_scrambler_handles_lists_correctly():
    data = {
        "documentState": "DRAFT",
        "id": "otm-123456",
        "universityOrgIds": [
            "otm-123456"
        ],
        "titles": [
            {
                "fi": "Finnish version",
                "sv": "Swedish version",
                "en": "English version"
            }
        ],
        "firstName": "string",
        "lastName": "string",
        "emailAddress": "string"
    }

    scrambled_data = KoriPersonScrambler.scramble(copy.deepcopy(data), set())
    list_keys = {'titles', 'universityOrgIds'}
    for key in list_keys:
        assert isinstance(scrambled_data[key], list), scrambled_data[key]

    PublicPerson.model_validate(scrambled_data)
