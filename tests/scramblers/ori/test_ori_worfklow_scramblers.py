import copy

import pytest

from funidata_utils.data_scramblers.workflow_scrambler import WorkflowScramblerSelector


@pytest.mark.unit
def test_module_att_workflow_scrambler_scrambles_customStudyDrafts():
    data = {
        'id': '1',
        'type': 'ModuleAttainmentWorkflow',
        'application': {
            'type': 'ModuleAttainmentApplication',
            "planContent": {
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
                ]
            }
        },
        'planContent': {
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
            ]
        }
    }

    scrambled_data = WorkflowScramblerSelector.scramble(copy.deepcopy(data), set())
    assert scrambled_data['planContent']['customStudyDrafts'][0]['name'] != data['planContent']['customStudyDrafts'][0]['name']
    assert scrambled_data['planContent']['customStudyDrafts'][0]['description'] != data['planContent']['customStudyDrafts'][0]['description']
    assert scrambled_data['planContent']['customStudyDrafts'][0]['location'] != data['planContent']['customStudyDrafts'][0]['location']

    assert scrambled_data['application']['planContent']['customStudyDrafts'][0]['name'] != data['application']['planContent']['customStudyDrafts'][0]['name']
    assert scrambled_data['application']['planContent']['customStudyDrafts'][0]['description'] != data['application']['planContent']['customStudyDrafts'][0][
        'description']
    assert scrambled_data['application']['planContent']['customStudyDrafts'][0]['location'] != data['application']['planContent']['customStudyDrafts'][0][
        'location']


@pytest.mark.unit
def test_module_att_scrambler_handles_empty_customStudyDrafts():
    data = {
        'id': '1',
        'type': 'ModuleAttainmentWorkflow',
        'application': {
            'type': 'ModuleAttainmentApplication',
            'planContent': {
                "customStudyDrafts": [],
            }
        },
        'planContent': {
            'type': 'ModuleAttainmentApplication',
            "customStudyDrafts": [],
        }
    }

    scrambled_data = WorkflowScramblerSelector.scramble(copy.deepcopy(data), set())
    assert scrambled_data['planContent'] == data['planContent']
    assert scrambled_data['application'] == data['application']


@pytest.mark.unit
def test_module_att_scrambler_handles_null_customStudyDrafts():
    data = {
        'id': '1',
        'type': 'ModuleAttainmentWorkflow',
        'application': {
            'type': 'ModuleAttainmentApplication',
            'planContent': {
                "customStudyDrafts": None,
            }
        },
        'planContent': {
            "customStudyDrafts": None,
        }
    }

    scrambled_data = WorkflowScramblerSelector.scramble(copy.deepcopy(data), set())
    assert scrambled_data['planContent'] == data['planContent']
    assert scrambled_data['application'] == data['application']
