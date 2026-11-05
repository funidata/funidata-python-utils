import copy
import re

import pytest

from funidata_utils.data_scramblers.attainment import AttainmentScrambler


@pytest.mark.unit
def test_attainment_scrambler_scrambles_acceptorPersons():
    data = {
        'id': '1',
        'acceptorPersons': [
            {'personId': None, 'text': 'Lars'},
            {'personId': '1', 'text': None}
        ]
    }

    scrambled_data = AttainmentScrambler.scramble(copy.deepcopy(data), set())
    assert len(scrambled_data['acceptorPersons']) == 2

    # The first person with a `text` name should be scrambled, the other one should not.
    assert scrambled_data['acceptorPersons'][0]['text'] != data['acceptorPersons'][0]['text']
    assert scrambled_data['acceptorPersons'][1]['text'] == data['acceptorPersons'][1]['text']


@pytest.mark.unit
def test_attainment_scrambler_handles_empty_acceptorPersons():
    data = {
        'id': '1',
        'acceptorPersons': []
    }

    scrambled_data = AttainmentScrambler.scramble(copy.deepcopy(data), set())


@pytest.mark.unit
def test_attainment_scrambler_handles_null_acceptorPersons():
    data = {
        'id': '1',
        'acceptorPersons': None
    }

    scrambled_data = AttainmentScrambler.scramble(copy.deepcopy(data), set())


@pytest.mark.unit
def test_attainment_scrambler_scrambles_CTI():
    data = {
        'id': '1',
        "creditTransferInfo": {
            "educationalInstitutionUrn": "urn:code:educational-institution:*",
            "internationalInstitutionUrn": "urn:code:international-institution:*",
            "organisation": "string",
            "creditTransferDate": "2026-09-04"
        },
    }

    scrambled_data = AttainmentScrambler.scramble(copy.deepcopy(data), set())
    # CTI organisation should be scrambled
    assert scrambled_data['creditTransferInfo']['organisation'] != data['creditTransferInfo']['organisation']


@pytest.mark.unit
def test_attainment_scrambler_handles_missing_CTI():
    data = {
        'id': '1',
        "creditTransferInfo": None
    }
    AttainmentScrambler.scramble(copy.deepcopy(data), set())


@pytest.mark.unit
def test_attainment_scrambler_scrambles_cooperationNetworkStatus():
    data = {
        'id': '1',
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
            "homeStudyRightId": "string"
        },
    }

    scrambled_data = AttainmentScrambler.scramble(copy.deepcopy(data), set())
    # Cooperation network rejection reason should be scrambled
    assert all(
        scrambled_data['cooperationNetworkStatus']['rejectionReason'].get(lang) != data['cooperationNetworkStatus']['rejectionReason'].get(lang)
            for lang in {'fi', 'en', 'sv'}
    )


@pytest.mark.unit
def test_attainment_scrambler_handles_missing_cooperation_network_status():
    data = {
        'id': '1',
        "cooperationNetworkStatus": None
    }
    AttainmentScrambler.scramble(copy.deepcopy(data), set())


@pytest.mark.unit
def test_attainment_scrambler_scrambles_person_fields_consistently_with_private_person():
    from funidata_utils.data_scramblers.private_person import PrivatePersonScrambler

    data = {
        'id': '1',
        'personId': 'otm-person-1',
        'personFirstNames': 'Matti Kalevi',
        'personLastName': 'Meikäläinen',
        'personStudentNumber': '012345678',
    }

    scrambled_data = AttainmentScrambler.scramble(copy.deepcopy(data), set())
    assert scrambled_data['personFirstNames'] != data['personFirstNames']
    assert scrambled_data['personLastName'] != data['personLastName']
    assert scrambled_data['personStudentNumber'] != data['personStudentNumber']
    assert re.fullmatch(r'[1-9a-z][0-9a-z]{8}', scrambled_data['personStudentNumber'])

    person = PrivatePersonScrambler.scramble(
        {
            'id': data['personId'],
            'firstNames': data['personFirstNames'],
            'lastName': data['personLastName'],
            'studentNumber': data['personStudentNumber'],
        },
        set()
    )
    assert scrambled_data['personFirstNames'] == person['firstNames']
    assert scrambled_data['personLastName'] == person['lastName']
    assert scrambled_data['personStudentNumber'] == person['studentNumber']


@pytest.mark.unit
def test_attainment_scrambler_handles_null_person_fields():
    data = {
        'id': '1',
        'personId': 'otm-person-1',
        'personFirstNames': None,
        'personLastName': None,
        'personStudentNumber': None,
    }

    scrambled_data = AttainmentScrambler.scramble(copy.deepcopy(data), set())
    assert scrambled_data['personFirstNames'] is None
    assert scrambled_data['personLastName'] is None
    assert scrambled_data['personStudentNumber'] is None


_PERSON_KEYS = ('personFirstNames', 'personLastName', 'personStudentNumber')


@pytest.mark.unit
def test_attainment_scrambler_person_fields_seed_on_personId():
    data = {
        'id': 'otm-1',
        'personId': 'person-1',
        'personFirstNames': 'Real First',
        'personLastName': 'Real Last',
        'personStudentNumber': '012345678',
    }
    other_attainment = {**data, 'id': 'otm-2'}

    scrambled = AttainmentScrambler.scramble(copy.deepcopy(data), set())
    scrambled_other = AttainmentScrambler.scramble(copy.deepcopy(other_attainment), set())

    for key in _PERSON_KEYS:
        assert scrambled[key] != data[key]
        # Same person on a different attainment gets the same pseudonym.
        assert scrambled[key] == scrambled_other[key]


@pytest.mark.unit
def test_attainment_scrambler_person_fields_without_personId_fall_back_to_id():
    data = {
        'id': 'otm-1',
        'personFirstNames': 'Real First',
        'personLastName': 'Real Last',
        'personStudentNumber': '012345678',
    }

    scrambled = AttainmentScrambler.scramble(copy.deepcopy(data), set())
    scrambled_again = AttainmentScrambler.scramble(copy.deepcopy(data), set())

    for key in _PERSON_KEYS:
        assert scrambled[key] != data[key]
        assert scrambled[key] == scrambled_again[key]


@pytest.mark.unit
def test_attainment_scrambler_handles_missing_rejectionReason():
    # rejectionReason is optional in SISU CooperationNetworkStatus
    data = {
        'id': 'otm-1',
        "cooperationNetworkStatus": {
            "direction": "OUTBOUND",
            "outboundStatus": "VALID",
            "cooperationNetworkId": "otm-123456",
        },
    }

    scrambled_data = AttainmentScrambler.scramble(copy.deepcopy(data), set())

    assert "rejectionReason" not in scrambled_data["cooperationNetworkStatus"]
    assert scrambled_data["cooperationNetworkStatus"] == data["cooperationNetworkStatus"]


@pytest.mark.unit
@pytest.mark.parametrize("rejection_reason", [
    {"fi": "Finnish version", "sv": "Swedish version", "en": "English version"},
    {"fi": "Finnish version", "sv": "Swedish version"},
    {"en": "English version"},
])
def test_attainment_scrambler_keeps_rejectionReason_language_keys(rejection_reason):
    data = {
        'id': 'otm-1',
        "cooperationNetworkStatus": {
            "direction": "INBOUND",
            "rejectionReason": rejection_reason,
        },
    }

    scrambled_data = AttainmentScrambler.scramble(copy.deepcopy(data), set())
    scrambled_reason = scrambled_data['cooperationNetworkStatus']['rejectionReason']

    assert isinstance(scrambled_reason, dict)
    assert set(scrambled_reason) == set(rejection_reason)
    for lang, original in rejection_reason.items():
        assert isinstance(scrambled_reason[lang], str) and scrambled_reason[lang]
        assert scrambled_reason[lang] != original
