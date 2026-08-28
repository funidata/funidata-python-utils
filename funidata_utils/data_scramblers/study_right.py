import logging
from typing import Tuple

from .utils.generic_scrambling import (
    scramble_with_weighted_pseudorandom,
)
from ..data_scramblers.base import SingletonMetaScrambler
from ..utils import update_inner_dictionary_key


logger = logging.getLogger(__name__)


class StudyRightScrambler(SingletonMetaScrambler):
    @classmethod
    def scramble(cls, entity: dict, processed_keys: dict) -> dict:
        """ Scramble StudyRight fields and add the scramblers to processed_keys """
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
            studyStartDate=None,  # Readonly attr
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
                        grantReason="Extension grant Raisin: Lorem Ipsum" if original_extension['grantReason'] else None,
                        deleteReason="Extension Delete Raisin: Lorem Ipsum" if original_extension['deleteReason'] else None
                    )
                    for original_extension in x.get('studyRightExtensions', []) or []
                ]
            ],
            studyRightCancellation=[
                (
                    update_inner_dictionary_key,
                    dict(
                        dot_separated_key='studyRightCancellation.cancellationReason',
                        new_value='studyRightCancellation.cancellationReason: Lorem Ipsum'
                    )
                ),
            ],
            studyRightPassivations=[
                lambda x: [
                    # Override grant + delete reasons with lorem ipsum, otherwise retain original extensions
                    lambda original_val: update_inner_dictionary_key(
                        original_passivation,
                        'additionalInfo',
                        'studyRightPassivations.additionalInfo: Lorem Ipsum'
                    )
                    for original_passivation in x.get('studyRightPassivations', []) or []
                ]
            ],
            studyRightTermination=[
                lambda original_val: update_inner_dictionary_key(
                    original_val,
                    'studyRightTermination.terminationReason',
                    'studyRightTermination.terminationReason: Lorem Ipsum'
                ),
            ],
            studyRightGraduation=None,
            acceptedSelectionPath=None,
            requestedSelectionPath=None,
            studyRightTransfer=[
                lambda original_val: update_inner_dictionary_key(
                    original_val,
                    'studyRightTransfer.transferComments',
                    'studyRightTransfer.transferComments: Lorem Ipsum',
                    missing_key_handler='skip',
                ),
            ],
            phase1MinorSelections=None,
            phase2MinorSelections=None,
            personalizedSelectionPath=[
                lambda original_val: update_inner_dictionary_key(
                    original_val,
                    'personalizedSelectionPath.phase1.rationale',
                    'personalizedSelectionPath.phase1.rationale: Lorem Ipsum'
                ),
                lambda original_val: update_inner_dictionary_key(
                    original_val,
                    'personalizedSelectionPath.phase2.rationale',
                    'personalizedSelectionPath.phase2.rationale: Lorem Ipsum',
                    missing_key_handler='skip',
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
                            ({'fi': 'additionalInformation: Lorem Ipsum'}, 1000),
                            ({'fi': 'Pallerojumppa'}, 42),
                        ],
                        scramble_seed_key=entity['id'],
                        scramble_empty_values=False
                    )
                )
            ],
            cooperationNetworkRights=None,
            cooperationNetworkStatus=[
                lambda original_val: update_inner_dictionary_key(
                    original_val,
                    dot_separated_key='cooperationNetworkStatus.rejectionReason',
                    new_value=None,
                    missing_key_handler='skip'
                ),
                lambda original_val: update_inner_dictionary_key(
                    original_val,
                    'cooperationNetworkStatus.outboundStatusMessage',
                    new_value=None,
                    missing_key_handler='skip'
                ),
            ],
            schoolEducationLanguageUrn=None,
        )

        for key, scramblers in scrambling_keys.items():
            processed_keys[key].append(scramblers)
            if not scramblers:
                continue

            for _scrambler in scramblers:
                if isinstance(_scrambler, Tuple):
                    entity[key] = _scrambler[0](entity=entity, **_scrambler[1])
                else:
                    entity[key] = _scrambler(entity)

        return entity
