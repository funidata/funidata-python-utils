from .replacement_data import thesis_titles_fi, thesis_titles_en, thesis_titles_sv
from .utils.generic_scrambling import replace_from_list
from ..data_scramblers.base import SingletonMetaScrambler
from ..utils import update_inner_dictionary_key


class MobilityPeriodScrambler(SingletonMetaScrambler):
    # key=None means "Keep the original value"
    # lambda x: None means -> set the value None
    scrambling_keys = dict(
        id=None,
        documentState=None,
        studyRightId=None,
        personId=None,
        mobilityDirection=None,
        activityPeriod=None,
        phase=None,
        mobilityProgramUrn=None,
        mobilityProgramDescription=[
            lambda x: 'mobilityProgramDescription' if x else x
        ],
        mobilityTypeUrn=None,
        countryUrn=None,
        internationalInstitutionUrn=None,
        organisation=[
            lambda x: 'organisation' if x else x,
        ],
        mobilityStudyRightTypeUrn=None,
        virtualMobilityType=None,
        isCancelled=None,
    )
