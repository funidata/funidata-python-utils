import copy

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
