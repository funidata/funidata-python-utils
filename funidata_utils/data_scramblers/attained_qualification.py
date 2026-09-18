from .utils.generic_scrambling import scramble_with_weighted_pseudorandom
from ..data_scramblers.base import SingletonMetaScrambler
from ..utils import update_inner_dictionary_key


class AttainedQualificationScrambler(SingletonMetaScrambler):
    # key=None means "Keep the original value"
    # lambda x: None means -> set the value None
    scrambling_keys = dict(
        id=None,
        documentState=None,
        qualificationId=None,
        personId=None,
        studyRightId=None,
        moduleGroupId=None,
        additionalInformation=[
            lambda entity: scramble_with_weighted_pseudorandom(
                entity=entity,
                key='additionalInformation',
                weights=[
                    ({'fi': 'additionalInformation: Lorem Ipsum'}, 1000),
                    ({'fi': 'Pallerojumppa'}, 42),
                ],
                scramble_seed_key=entity['id'],
                scramble_empty_values=False
            )
        ],
        associatedStudies=[
            lambda x: update_inner_dictionary_key(
                x,
                'associatedStudies.description',
                new_value='associatedStudies.description',
                missing_key_handler='skip'
            )
        ],
        attainmentDate=None,
        studyFieldUrn=None,
        attainmentMethod=None,
        credits=None,
        attainmentIds=None,
        childAttainedQualificationIds=None,
        registrationDate=None,
        verifierPersonId=None,
    )
