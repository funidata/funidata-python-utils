from ..data_scramblers.base import SingletonMetaScrambler
from ..utils import update_inner_dictionary_key
from .utils.generic_scrambling import scramble_localized_string




class IlmoEnrolmentScrambler(SingletonMetaScrambler):
    scrambling_keys = dict(
        id=None,
        documentState=None,
        personId=None,
        courseUnitRealisationId=None,
        courseUnitId=None,
        assessmentItemId=None,
        studyRightId=None,
        openUniversityCartId=None,
        openUniversityCartItemId=None,
        status=None,
        state=None,
        processingState=None,
        studySubGroups=None,
        studyGroupSets=None,
        confirmedStudySubGroupIds=None,
        tentativeStudySubGroupIds=None,
        enrolmentDateTime=None,
        isInCalendar=None,
        colorIndex=None,
        quotaIds=None,
        activeQuotaId=None,
        allocatedQuotaId=None,
        maximumQuotaIds=None,
        enrolmentRightId=None,
        replacedByEnrolmentId=None,
        cooperationNetworkStatus=[
            lambda original_val: update_inner_dictionary_key(
                original_val,
                dot_separated_key='cooperationNetworkStatus.rejectionReason',
                new_value=(
                    scramble_localized_string,
                    dict(
                        key='rejectionReason',
                        weights=[
                            ({'fi': 'cooperationNetworkStatus.rejectionReason'}, 1000),
                            ({'fi': 'Pallerojumppa'}, 42),
                        ],
                        scramble_seed_key=original_val['id'],
                        scramble_empty_values=False
                    )
                ),
                missing_key_handler='skip'
            ),
            lambda original_val: update_inner_dictionary_key(
                original_val,
                'cooperationNetworkStatus.outboundStatusMessage',
                new_value='cooperationNetworkStatus.outboundStatusMessage',
                missing_key_handler='skip'
            ),
            lambda original_val: update_inner_dictionary_key(
                original_val,
                'cooperationNetworkStatus.selectionItemStatusInfo',
                new_value='cooperationNetworkStatus.selectionItemStatusInfo',
                missing_key_handler='skip'
            ),
        ],
        studentConsentForOutboundDataTransfer=[
            lambda original_val: update_inner_dictionary_key(
                original_val,
                dot_separated_key='studentConsentForOutboundDataTransfer.clause',
                new_value='studentConsentForOutboundDataTransfer.clause: scrambled',
                missing_key_handler='skip'
            ),
        ],
    )
