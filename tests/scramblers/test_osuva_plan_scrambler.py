import copy

import pytest

from funidata_utils.data_scramblers.osuva_plan_scrambler import OsuvaPlanScrambler


@pytest.mark.unit
def test_osuva_scrambler_scrambles_name():
    data = {
        'id': '1',
        "name": "string",
    }

    scrambled_data = OsuvaPlanScrambler.scramble(copy.deepcopy(data), set())

    assert scrambled_data['name'] != data['name']


@pytest.mark.unit
def test_attainment_scrambler_scrambles_customStudyDrafts():
    data = {
        'id': '1',
        "customStudyDrafts": [
            {
                "id": "otm-123456",
                "parentModuleId": "otm-123456",
                "name": "string",
                "description": "string",
                "location": "string",
                "credits": 0,
                "plannedPeriods": [
                    "string"
                ]
            }
        ],
    }

    scrambled_data = OsuvaPlanScrambler.scramble(copy.deepcopy(data), set())
    assert scrambled_data['customStudyDrafts'][0]['name'] != data['customStudyDrafts'][0]['name']
    assert scrambled_data['customStudyDrafts'][0]['description'] != data['customStudyDrafts'][0]['description']
    assert scrambled_data['customStudyDrafts'][0]['location'] != data['customStudyDrafts'][0]['location']


@pytest.mark.unit
def test_attainment_scrambler_handles_empty_customStudyDrafts():
    data = {
        'id': '1',
        "customStudyDrafts": [],
    }

    scrambled_data = OsuvaPlanScrambler.scramble(copy.deepcopy(data), set())


@pytest.mark.unit
def test_attainment_scrambler_handles_null_customStudyDrafts():
    data = {
        'id': '1',
        "customStudyDrafts": None,
    }

    scrambled_data = OsuvaPlanScrambler.scramble(copy.deepcopy(data), set())
