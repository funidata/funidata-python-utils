import logging
from typing import Tuple

from .utils.generic_scrambling import (
    scramble_with_weighted_pseudorandom,
)
from ..data_scramblers.base import SingletonMetaScrambler
from ..utils import update_inner_dictionary_key


logger = logging.getLogger(__name__)


class AttainmentScrambler(SingletonMetaScrambler):
    scrambling_keys = dict(
        id=None,
        documentState=None,
        personId=None,
        verifierPersonId=None,
        studyRightId=None,
        registrationDate=None,
        expiryDate=None,
        attainmentLanguageUrn=None,
        # [ # Could be scrambled in theory, but probably best to not for now.
        #     lambda entity: scramble_with_weighted_pseudorandom(
        #         entity=entity,
        #         key='attainmentLanguageUrn',
        #         weights={
        #             'urn:code:language:fi': 1000,
        #             'urn:code:language:en': 300,
        #             'urn:code:language:sv': 50,
        #         },
        #         scramble_seed_key=entity['id']
        #     )
        # ],
        acceptorPersons=[
            lambda entity: update_inner_dictionary_key(
                entity,
                dot_separated_key='acceptorPersons.text',
                new_value=(
                    scramble_with_weighted_pseudorandom,
                    dict(
                        key='text',
                        weights=[
                            ({'fi': 'acceptorPersons.text: Kalle'}, 1000),
                            ({'fi': 'acceptorPersons.text: Olle'}, 1000),
                            ({'fi': 'Niskaterapia'}, 42),
                            ({'fi': 'Alaraaja'}, 42),
                        ],
                        scramble_seed_key=entity['id'],
                        scramble_empty_values=False
                    )
                ),
                missing_key_handler='skip'
            ),
        ],
        organisations=None,
        state=None,
        misregistration=None,
        misregistrationRationale=[
            lambda x: "misregistrationRationale" if x['misregistrationRationale'] else None,
        ],
        primary=None,
        credits=None,
        studyWeeks=None,
        gradeScaleId=None,
        gradeId=None,
        gradeAverage=None,
        additionalInfo=[
            lambda x: {
                "fi": "Suorituksen lisätiedot",
                "en": "Attainments additional information",
                "sv": "Tillägsinformation om prestationen",
            } if x['additionalInfo'] else None,
        ],
        administrativeNote=[
            lambda x: "administrativeNote" if x['administrativeNote'] else None,
        ],
        studyFieldUrn=None,
        workflowId=None,
        moduleContentApplicationId=None,
        creditTransferInfo=[
            lambda entity: update_inner_dictionary_key(
                entity,
                dot_separated_key='creditTransferInfo.organisation',
                new_value=(
                    scramble_with_weighted_pseudorandom,
                    dict(
                        key='organisation',
                        weights=[
                            ({'fi': 'creditTransferInfo.organisation'}, 1000),
                            ({'fi': 'Pallerojumppa'}, 42),
                        ],
                        scramble_seed_key=entity['id'],
                        scramble_empty_values=False
                    )
                ),
                missing_key_handler='skip'
            ),
        ],
        cooperationNetworkStatus=[
            lambda entity: update_inner_dictionary_key(
                entity,
                dot_separated_key='cooperationNetworkStatus.rejectionReason',
                new_value=(
                    scramble_with_weighted_pseudorandom,
                    dict(
                        key='rejectionReason',
                        weights=[
                            ({'fi': 'cooperationNetworkStatus.rejectionReason'}, 1000),
                            ({'fi': 'Pallerojumppa'}, 42),
                        ],
                        scramble_seed_key=entity['id'],
                        scramble_empty_values=False
                    )
                ),
                missing_key_handler='skip'
            ),
        ],
        rdiCredits=None,
        collaborationInstitution=None,
        enrolmentRightId=None,
        type=None,
        attainmentDate=None,
        s2r2Classification=None,

        # CUA
        courseUnitId=None,
        courseUnitGroupId=None,
        resolutionRationale=[
            lambda x: "resolutionRationale" if x.get('resolutionRationale') else None,
        ],
        evaluationCriteria=[
            lambda x: {
                "fi": "Suorituksen evaluationCriteria",
                "en": "Attainments evaluationCriteria",
                "sv": "evaluationCriteria om prestationen",
            } if x['evaluationCriteria'] else None,
        ],
        assessmentItemAttainmentIds=None,

        # CCUA
        name=None,
        studyLevelUrn=None,
        courseUnitTypeUrn=None,
        code=None,
        customStudyDraftId=None,

        # DPA / SMA / CSMA
        nodes=None,
        moduleId=None,
        moduleGroupId=None,
        embeddedModules=None,
        acceptorOrganisationIds=None,
        educationClassificationUrn=None,
        secondaryEducationClassificationUrn=None,
        degreeTitleUrn=None,
        honoraryTitleUrn=None,
        internationalContractualDegree=None,

        # AIA
        assessmentItemId=None,
        courseUnitRealisationId=None,

    )
