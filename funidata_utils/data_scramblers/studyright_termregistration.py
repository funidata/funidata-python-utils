from ..data_scramblers.base import SingletonMetaScrambler


class StudyRightTermRegistrationScrambler(SingletonMetaScrambler):
    # Only scramble Metadata, rest is safe.

    # key=None means "Keep the original value"
    # lambda x: None means -> set the value None
    scrambling_keys = dict(
        studyRightId=None,
        documentState=None,
        studentId=None,
        termRegistrations=None,
        statePeriods=None,
        statePeriodOverrides=None,
        state=None,
    )
