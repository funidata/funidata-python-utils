from .utils.generic_scrambling import scramble_with_weighted_pseudorandom
from .utils.key_scramblers import (
    get_scrambled_first_name, get_scrambled_last_name, get_scrambled_email,
)
from ..data_scramblers.base import SingletonMetaScrambler
from ..utils import update_inner_dictionary_key


class OsuvaPlanScrambler(SingletonMetaScrambler):
    # key=None means "Keep the original value"
    # lambda x: None means -> set the value None
    scrambling_keys = dict(
        id=None,
        documentState=None,
        universityOrgIds=None,
        rootId=None,
        learningOpportunityId=None,
        userId=None,
        name=[
            lambda entity: scramble_with_weighted_pseudorandom(
                entity=entity,
                key='name',
                weights=[
                    ('Lorem Ipsum suunitelma', 1000),
                    ('Opintoni suunitelmat', 42),
                    ('Suunnittelin opiskella', 42),
                    ('Voisin opiskella', 42),
                    ('Opintosuunnitelmani', 42),
                ],
                scramble_seed_key=entity['id'],
                scramble_empty_values=False
            )
        ],
        curriculumPeriodId=None,
        moduleSelections=None,
        courseUnitSelections=None,
        customModuleAttainmentSelections=None,
        customCourseUnitAttainmentSelections=None,
        assessmentItemSelections=None,
        timelineNotes=[
            lambda x: []
        ],
        customStudyDrafts=[
            lambda entity: update_inner_dictionary_key(
                entity,
                dot_separated_key='customStudyDrafts.name',
                new_value=(
                    scramble_with_weighted_pseudorandom,
                    dict(
                        key='name',
                        weights=[
                            ('Lorem Ipsum jakso', 1000),
                            ('Opintojaksoni', 42),
                            ('Suunniteltu jakso', 42),
                        ],
                        scramble_seed_key=entity['id'],
                        scramble_empty_values=False
                    )
                ),
                missing_key_handler='skip'
            ),
            lambda entity: update_inner_dictionary_key(
                entity,
                dot_separated_key='customStudyDrafts.description',
                new_value=(
                    scramble_with_weighted_pseudorandom,
                    dict(
                        key='description',
                        weights=[
                            ('Opin Lorem Ipsum', 1000),
                            ('Opintotavoitteeni', 42),
                            ('Suunniteltu osaamisen saavuttaminen', 42),
                        ],
                        scramble_seed_key=entity['id'],
                        scramble_empty_values=False
                    )
                ),
                missing_key_handler='skip'
            ),
            lambda entity: update_inner_dictionary_key(
                entity,
                dot_separated_key='customStudyDrafts.location',
                new_value=(
                    scramble_with_weighted_pseudorandom,
                    dict(
                        key='location',
                        weights=[
                            ('Lorem Ipsum sali', 500),
                            ('Lorem Ipsum korkeakoulu', 500),
                            ('Pallerojumppa', 42),
                        ],
                        scramble_seed_key=lambda _x: entity['id'] + _x['id'],
                        scramble_empty_values=False
                    )
                ),
                missing_key_handler='skip'
            ),
        ],
        primary=None,
        graduationSurveyOpenedOn=None,
        graduationSurveyDegreeProgrammeId=None,
    )
