from ..data_scramblers.base import SingletonMetaScrambler
from ..utils import update_inner_dictionary_key




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
        studentConsentForOutboundDataTransfer=[
            lambda original_val: update_inner_dictionary_key(
                original_val,
                dot_separated_key='studentConsentForOutboundDataTransfer.clause',
                new_value='studentConsentForOutboundDataTransfer.clause: scrambled',
                missing_key_handler='skip'
            ),
        ],
    )
