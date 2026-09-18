from ..data_scramblers.base import SingletonMetaScrambler


class TuitionFeeObligationPeriodScrambler(SingletonMetaScrambler):
    # key=None means "Keep the original value"
    # lambda x: None means -> set the value None
    scrambling_keys = dict(
        id=None,
        documentState=None,
        studyRightId=None,
        valid=None,
        tuitionFee=None,
        exempt=None,
        additionalInfo=[
            lambda x: {
                'fi': 'lisätiedot',
                'sv': 'tillägsinformation',
                'en': 'additional information'
            } if x else None
        ],
    )
