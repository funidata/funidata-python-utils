from .replacement_data import thesis_titles_fi, thesis_titles_en, thesis_titles_sv
from .utils.generic_scrambling import replace_from_list
from ..data_scramblers.base import SingletonMetaScrambler
from ..utils import update_inner_dictionary_key


class ThesisScrambler(SingletonMetaScrambler):
    # key=None means "Keep the original value"
    # lambda x: None means -> set the value None
    scrambling_keys = dict(
        id=None,
        documentState=None,
        personId=None,
        attainmentId=None,
        title=[
            lambda x: update_inner_dictionary_key(
                x,
                'title.fi',
                lambda y: replace_from_list(
                    original_value=x['id'],
                    replacement_list=thesis_titles_fi
                ),
                missing_key_handler='skip'
            ),
            lambda x: update_inner_dictionary_key(
                x,
                'title.en',
                lambda y: replace_from_list(
                    original_value=x['id'],
                    replacement_list=thesis_titles_en
                ),
                missing_key_handler='skip'
            ),
            lambda x: update_inner_dictionary_key(
                x,
                'title.sv',
                lambda y: replace_from_list(
                    original_value=x['id'],
                    replacement_list=thesis_titles_sv
                ),
                missing_key_handler='skip'
            )
        ],
        subject=[
            lambda x: {'fi': 'aihe', 'sv': 'ämne', 'en': 'subject'}
        ],
        thesisTypeUrn=None,
        responsibilityInfos=[ lambda x: [] ], # TODO: Update with real scrambling
        organisations=None,
        courseUnitId=None,
        courseUnitGroupId=None,
        state=None,
        publicInspectionDate=None,
        commissionType=None
    )
