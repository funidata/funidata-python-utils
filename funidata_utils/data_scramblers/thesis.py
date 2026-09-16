from ..data_scramblers.base import SingletonMetaScrambler


class ThesisScrambler(SingletonMetaScrambler):
    # key=None means "Keep the original value"
    # lambda x: None means -> set the value None
    scrambling_keys = dict(
        id=None,
        personId=None,
        attainmentId=None,
        title=None,
        subject=None,
        thesisTypeUrn=None,
        responsibilityInfos=None,
        organisations=None,
        courseUnitId=None,
        courseUnitGroupId=None,
        state=None,
        publicInspectionDate=None,
        commissionType=None
    )
