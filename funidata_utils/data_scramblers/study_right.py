import logging
from typing import Tuple, Any

from .utils.generic_scrambling import (
    scramble_with_weighted_pseudorandom, hashlib_hash, get_random_date,
)
from .utils.key_scramblers import (
    get_scrambled_first_name, get_scrambled_last_name, get_scrambled_nationalities, get_phone_number_shuffled_with_mask,
    get_scrambled_email,
)
from ..data_scramblers.base import SingletonMetaScrambler


logger = logging.getLogger(__name__)


def recursive_dict_fetch(
    entity: dict,
    keys: list
):
    if len(keys) == 1:
        return entity[keys[0]]

    return recursive_dict_fetch(entity[keys[0]], keys[1:])


def _dict_update_by_key_split(
    entity: dict,
    keys: list,
    new_value
):
    _first_key = keys[0]
    if _first_key not in entity:
        return None

    if entity[_first_key] is None:
        return None

    _current_entity_ref = entity
    for _key in keys[:-1]:
        if _current_entity_ref is None:
            return None

        if not isinstance(_current_entity_ref, dict):
            raise ValueError(f"Expected nested dictionaries, {_key} value is not a dict")

        _current_entity_ref = _current_entity_ref[_key]

    if not isinstance(_current_entity_ref, dict):
        raise ValueError(f"Expected nested dictionaries, {_key} value is not a dict")

    final_key = keys[-1]
    if final_key not in _current_entity_ref:
        raise KeyError(f"Key {final_key} not found")

    _current_entity_ref[final_key] = new_value

    return entity


def update_inner_dictionary_key(
    entity: dict,
    dot_separated_key: str,
    new_value: Any,
):
    parts = dot_separated_key.split('.')
    if not parts:
        raise ValueError("dot_separated_key required")

    diu = _dict_update_by_key_split(entity, parts, new_value)
    if diu is None:
        return None

    return entity.get(parts[0])


class StudyRightScrambler(SingletonMetaScrambler):
    @classmethod
    def scramble(cls, entity: dict) -> dict:
        """ Only allow returning keys that have been verified to be scramble-able or non-scrambleable!"""
        _out_entity = {}

        # key=None means "Keep the original value"
        # lambda x: None means -> set the value None
        scrambling_keys = dict(
            id=None,
            documentState=None,
            snapshotDateTime=None,
            studentId=None,
            educationId=None,
            organisationId=None,
            learningOpportunityId=None,
            admissionTargetId=None,
            admissionIdentifier=None,
            decreeOnUniversityDegreesUrn=None,
            studyRightExpirationRulesUrn=None,
            degreeRegulations=None,
            valid=None,
            grantDate=None,
            studyStartDate=[  # Readonly attr
                lambda x: None
            ],
            alternativeStudyStartDate=None,
            transferOutDate=None,
            transferOutUniversityUrn=None,
            homeOrganisationUrn=None,
            termRegistrations=[  # Readonly attr
                lambda x: None
            ],
            studyRightExtensions=[
                lambda x: [
                    # Override grant + delete reasons with lorem ipsum, otherwise retain original extensions
                    original_extension | dict(
                        grantReason="Lorem Ipsum" if original_extension['grantReason'] else None,
                        deleteReason="Lorem Ipsum" if original_extension['deleteReason'] else None
                    )
                    for original_extension in x.get('studyRightExtensions', []) or []
                ]
            ],
            studyRightCancellation=[
                lambda original_val: update_inner_dictionary_key(
                    original_val,
                    'studyRightCancellation.cancellationReason',
                    'Lorem Ipsum'
                ),
            ],
            studyRightPassivations=[
                lambda x: [
                    # Override grant + delete reasons with lorem ipsum, otherwise retain original extensions
                    lambda original_val: update_inner_dictionary_key(
                        original_passivation,
                        'additionalInfo',
                        'Lorem Ipsum'
                    )
                    for original_passivation in x.get('studyRightPassivations', []) or []
                ]
            ],
            studyRightTermination=[
                lambda original_val: update_inner_dictionary_key(
                    original_val,
                    'studyRightTermination.terminationReason',
                    'Lorem Ipsum'
                ),
            ],
            studyRightGraduation=None,
            acceptedSelectionPath=None,
            requestedSelectionPath=None,
            studyRightTransfer=[
                lambda original_val: update_inner_dictionary_key(
                    original_val,
                    'studyRightTransfer.transferComments',
                    'Lorem Ipsum'
                ),
            ],
            phase1MinorSelections=None,
            phase2MinorSelections=None,
            personalizedSelectionPath=[
                lambda original_val: update_inner_dictionary_key(
                    original_val,
                    'personalizedSelectionPath.phase1.rationale',
                    'Lorem Ipsum'
                ),
                lambda original_val: update_inner_dictionary_key(
                    original_val,
                    'personalizedSelectionPath.phase1.rationale',
                    'Lorem Ipsum'
                ),
            ],
            courseUnitSelections=None,
            moduleSelections=None,
            studyFieldUrn=None,
            phase1EducationClassificationUrn=None,
            phase2EducationClassificationUrn=None,
            phase1EducationClassificationLocked=None,
            phase2EducationClassificationLocked=None,
            fundingSourceUrn=None,
            phase1QualificationUrns=None,
            phase2QualificationUrns=None,
            phase1EducationLocationUrn=None,
            phase2EducationLocationUrn=None,
            phase1InternationalContractualDegree=None,
            phase2InternationalContractualDegree=None,
            admissionTypeUrn=None,
            codeUrns=None,
            additionalInformation=[
                (
                    scramble_with_weighted_pseudorandom,
                    dict(
                        key='additionalInformation',
                        weights=[
                            (None, 2500),
                            ({'fi': 'Lorem Ipsum'}, 1000),
                            ({'fi': 'Pallerojumppa'}, 42),
                        ],
                        scramble_seed_key=entity['id']
                    )
                )
            ],
            cooperationNetworkRights=None,
            cooperationNetworkStatus=None,
            schoolEducationLanguageUrn=None,
        )

        for key, scramblers in scrambling_keys.items():
            if not scramblers:
                _out_entity[key] = entity.get(key)
            else:
                for _scrambler in scramblers:
                    if isinstance(_scrambler, Tuple):
                        _out_entity[key] = _scrambler[0](entity=entity, **_scrambler[1])
                    else:
                        _out_entity[key] = _scrambler(entity)

        return _out_entity
