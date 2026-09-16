import logging
import sys

from .utils.generic_scrambling import scramble_with_weighted_pseudorandom, random_shuffle, get_string_shuffled_with_mask
from .utils.key_scramblers import get_scrambled_first_name, get_scrambled_last_name
from ..data_scramblers.base import SingletonMetaScrambler
from ..utils import update_inner_dictionary_key


logger = logging.getLogger(__name__)


def _handle_custom_study_drafts(_customStudyDraft):
    update_inner_dictionary_key(
        _customStudyDraft,
        dot_separated_key='name',
        new_value='name',
        missing_key_handler='skip'
    )
    update_inner_dictionary_key(
        _customStudyDraft,
        dot_separated_key='description',
        new_value='description',
        missing_key_handler='skip'
    )
    update_inner_dictionary_key(
        _customStudyDraft,
        dot_separated_key='location',
        new_value='location',
        missing_key_handler='skip'
    )

    return _customStudyDraft


def _handle_application_scrambling(original_application):
    if not original_application:
        return original_application

    application_type = original_application['type']

    # save some CPU time going by discriminator instead of processing all possible keys
    # Base class includes following for all types:
    # localId
    # creationTime
    # createdByPersonId
    # organisations - no freeform text entry option
    # type

    match application_type:
        case 'StudentWorkflowApplication':
            # bool mustPrintDecision - no scrambling
            pass

        case 'AttainmentWorkflowApplication':
            # extends StudentWorkflowApplication
            # str planId - no scrambling
            # str studyRightId - no scrambling
            pass

        case 'ModuleContentWorkflowApplication':
            # extends StudentWorkflowApplication
            # str educationId - no scrambling
            # str studyRightId - no scrambling
            # str parentModuleId - no scrambling
            # str approvedModuleId - no scrambling
            # str originalReferredPlanId - no scrambling
            original_application['applicationRationale'] = update_inner_dictionary_key(
                original_application,
                'applicationRationale',
                'applicationRationale',
                missing_key_handler='skip'
            )
            # list[str] moduleSelections - no scrambling
            # list[str] courseUnitSelections - no scrambling
            # list[str] customModuleAttainmentSelections - no scrambling
            # list[str] customCourseUnitAttainmentSelections - no scrambling
            update_inner_dictionary_key(
                original_application,
                'customStudyDrafts',
                new_value=_handle_custom_study_drafts,
                missing_key_handler='skip'
            )

        case 'StudyRightExtensionApplication':
            # extends StudentWorkflowApplication
            # str planId - no scramble
            update_inner_dictionary_key(
                original_application,
                'planSnapshot.customStudyDrafts',
                new_value=_handle_custom_study_drafts,
                missing_key_handler='skip'
            )
            original_application['planSnapshot'] = original_application['planSnapshot'] | dict(
                name='name',
                timelineNotes=[],
            )
            # str studyRightId - no scramble
            # str educationId - no scramble
            # studyRightValidity - no scramble
            original_application['previousExtensions'] = [
                _extension | dict(
                    grantReason='grantReason',
                    deleteReason='deleteReason',
                )
                for _extension in original_application.get('previousExtensions')
            ] if original_application['previousExtensions'] else original_application['previousExtensions']  # leave as-is if empty list or null
            # termRegistrations - list of non-scrambleable data
            # int usedAttendanceTerms - no scramble
            # int usedAbsenceTerms - no scramble
            # int usedStatutoryAbsenceTerms - no scramble
            # int termsWithoutRegistration - no scramble
            # attainmentIds - no scramble
            # phase1Progress - theoreticall contains phase1Progress['phaseName'] but sounds like it'll be education phase name, not manual entry
            # phase2Progress - theoreticall contains phase2Progress['phaseName'] but sounds like it'll be education phase name, not manual entry
            # int requestedTerms - no scramble
            original_application['delayRationale'] = 'delayRationale'  # not-nullable so no null handling
            original_application['applicationRationale'] = 'applicationRationale'  # not-nullable so no null handling

        case 'PriorLearningInclusionApplication':
            # mustPrintDecision
            # planId
            # studyRightId
            original_application['priorLearnings'] = [
                x | dict(
                    name='name',
                    organisation='organisation',
                    description='description',
                    gradeScale='Grade scale 1-5',
                    credits=scramble_with_weighted_pseudorandom(
                        x,
                        key='credits',
                        weights=[
                            ("30 op", 50),
                            ("15 op", 100),
                            ("5 op", 150),
                            ("5 ov", 25),
                            ("2 pallerojumppaa", 5),
                        ],
                        scramble_seed_key=lambda x: x['localId'],
                        scramble_empty_values=False,
                        missing_key_handler='skip'
                    ),
                    grade=scramble_with_weighted_pseudorandom(
                        x,
                        key='grade',
                        weights=[
                            ("5", 100),
                            ("4", 250),
                            ("3", 500),
                            ("1", 350),
                        ],
                        scramble_seed_key=lambda x: x['localId'],
                        scramble_empty_values=False,
                        missing_key_handler='skip'
                    )
                )
                for x in
                original_application['priorLearnings']
            ]
            original_application['name'] = 'name'
            # plannedParentModuleId
            # degreeProgrammeId
            # degreeProgrammeGroupId
            if 'customStudyDrafts' in original_application:
                update_inner_dictionary_key(
                    original_application,
                    'customStudyDrafts',
                    new_value=_handle_custom_study_drafts,
                    missing_key_handler='skip'
                )
            # moduleGroupId
            # moduleId

        case 'PriorLearningSubstitutionApplication':
            # str courseUnitId - no scramble
            # str courseUnitGroupId - no scramble
            original_application['priorLearnings'] = [
                x | dict(
                    name='name',
                    organisation='organisation',
                    description='description',
                    gradeScale='Grade scale 1-5',
                    credits=scramble_with_weighted_pseudorandom(
                        x,
                        key='credits',
                        weights=[
                            ("30 op", 50),
                            ("15 op", 100),
                            ("5 op", 150),
                            ("5 ov", 25),
                            ("2 pallerojumppaa", 5),
                        ],
                        scramble_seed_key=lambda x: x['localId'],
                        scramble_empty_values=False,
                        missing_key_handler='skip'
                    ),
                    grade=scramble_with_weighted_pseudorandom(
                        x,
                        key='grade',
                        weights=[
                            ("5", 100),
                            ("4", 250),
                            ("3", 500),
                            ("1", 350),
                        ],
                        scramble_seed_key=lambda x: x['localId'],
                        scramble_empty_values=False,
                        missing_key_handler='skip'
                    )
                )
                for x in
                original_application['priorLearnings']
            ]

        case 'ModuleAttainmentApplication':
            update_inner_dictionary_key(
                original_application,
                'planContent.customStudyDrafts',
                new_value=_handle_custom_study_drafts,
                missing_key_handler='skip'
            )

        case 'CustomAttainmentApplication':
            # mustPrintDecision
            # planId
            # studyRightId
            original_application['name'] = 'name'
            # plannedParentModuleId
            # degreeProgrammeId
            # degreeProgrammeGroupId
            original_application['responsibleTeacher'] = 'responsibleTeacher'
            original_application['applicationRationale'] = 'applicationRationale'
            original_application['attainmentDescription'] = 'attainmentDescription'
            # plannedCredits
            update_inner_dictionary_key(
                original_application,
                'customStudyDrafts',
                new_value=_handle_custom_study_drafts,
                missing_key_handler='skip'
            )
            # attainmentLanguage
            # moduleGroupId[...]
            # moduleId[...]

        case 'DegreeProgrammeAttainmentApplication':
            # mustPrintDecision
            # planId
            # studyRightId
            # moduleId
            # moduleGroupId
            update_inner_dictionary_key(
                original_application,
                'planContent.customStudyDrafts',
                new_value=_handle_custom_study_drafts,
                missing_key_handler='skip'
            )
            original_application['degreeDeliveryMethod'] = scramble_with_weighted_pseudorandom(
                original_application,
                'degreeDeliveryMethod',
                weights={'PICK_UP': 1337, 'DIGITAL_CERTIFICATE': 4242},
                scramble_seed_key=original_application['localId']
            )
            original_application['deliveryAddress'] = None
            original_application['additionalInfo'] = 'additionalInfo'
            # joinsAlumniAssociation

            original_application['questionnaireAnswers'] = [
                _answer | dict(
                    answer=scramble_with_weighted_pseudorandom(
                        _answer,
                        'answer',
                        weights={'An answer to question': 1337, 'Yes': 4242},
                        scramble_seed_key=_answer['answer']
                    ),
                    question=scramble_with_weighted_pseudorandom(
                        _answer,
                        key='question',
                        weights=[
                            ({'fi': 'Nautitko banaani', 'en': 'Do you like bananas'}, 500),
                            ({'fi': 'Haluatko avokaado', 'en': 'Would you like an avocado'}, 500),
                            ({'fi': 'Haluatko ostaa hampurilainen', 'en': 'Would you like to buy an amburger'}, 500),
                        ],
                        scramble_seed_key=_answer['question']
                    ),
                    guidance=scramble_with_weighted_pseudorandom(
                        _answer,
                        key='guidance',
                        weights=[
                            ({'fi': 'Tämä on <b>tärkeää</b> tietää.', 'en': 'This is <b>important</b> to know.'}, 500),
                            ({'fi': 'Pakollinen kysymys', 'en': 'This question is mandatory'}, 500),
                            ({'fi': 'Sinapilla?', 'en': 'With mustard?'}, 500),
                        ],
                        scramble_seed_key=_answer['guidance']
                    )
                )
                for _answer in original_application['questionnaireAnswers']
            ] if original_application['questionnaireAnswers'] else original_application['questionnaireAnswers']

        case 'CustomModuleContentApplication' | 'RequiredModuleContentApplication':
            # mustPrintDecision
            # educationId
            # studyRightId
            # parentModuleId
            # approvedModuleId
            # originalReferredPlanId
            original_application['applicationRationale'] = update_inner_dictionary_key(
                original_application,
                'applicationRationale',
                'applicationRationale',
                missing_key_handler='skip'
            )
            # moduleSelections
            # courseUnitSelections
            # customModuleAttainmentSelections
            # customCourseUnitAttainmentSelections
            update_inner_dictionary_key(
                original_application,
                'customStudyDrafts',
                new_value=_handle_custom_study_drafts,
                missing_key_handler='skip'
            )

        case _:
            raise Exception(f"Unknown application type {application_type}")

    return original_application


def _handle_decision_scrambling(original_decision):
    if not original_decision:
        return original_decision

    decision_type = original_decision['type']

    # shared keys:
    # state
    # registeredBy
    # approvedBy
    original_decision['approverTitle'] = {'fi': 'approverTitle'} if original_decision['approverTitle'] else None
    # approvalDate
    original_decision['resolutionRationale'] = 'resolutionRationale'

    match decision_type:
        case 'AttainmentWorkflowDecision' | 'ModuleContentWorkflowDecision':
            for recommendation in {'formalRecommendation', 'contentRecommendation'}:
                update_inner_dictionary_key(
                    original_decision,
                    dot_separated_key=f'{recommendation}.responsiblePerson',
                    new_value=f'{recommendation}.responsiblePerson',
                    missing_key_handler='skip'
                )
                update_inner_dictionary_key(
                    original_decision,
                    dot_separated_key=f'{recommendation}.responsiblePersonTitle',
                    new_value={'fi': f'{recommendation}.responsiblePersonTitle'},
                    missing_key_handler='skip'
                )
                update_inner_dictionary_key(
                    original_decision,
                    dot_separated_key=f'{recommendation}.additionalInformation',
                    new_value=f'{recommendation}.additionalInformation',
                    missing_key_handler='skip'
                )
                update_inner_dictionary_key(
                    original_decision,
                    dot_separated_key=f'{recommendation}.comment',
                    new_value=f'{recommendation}.comment',
                    missing_key_handler='skip'
                )
            if decision_type == 'AttainmentWorkflowDecision':
                original_decision['appealInstructions'] = update_inner_dictionary_key(
                    original_decision,
                    dot_separated_key='appealInstructions',
                    new_value='appealInstructions',
                    missing_key_handler='skip'
                )
            if decision_type == 'ModuleContentWorkflowDecision':
                original_decision['conditionalApprovalTerms'] = update_inner_dictionary_key(
                    original_decision,
                    dot_separated_key='conditionalApprovalTerms',
                    new_value='conditionalApprovalTerms',
                    missing_key_handler='skip'
                )

        case 'RevokedWorkflowDecision':
            # Does not appear to require scrambling in addition to "base"
            pass

        case 'StudyRightExtensionWorkflowDecision':
            # AdministrativeReview
            update_inner_dictionary_key(
                original_decision,
                dot_separated_key='administrativeReview.result',
                new_value='administrativeReview.result',
                missing_key_handler='skip'
            )
            update_inner_dictionary_key(
                original_decision,
                dot_separated_key='administrativeReview.notes',
                new_value='administrativeReview.notes',
                missing_key_handler='skip'
            )
            update_inner_dictionary_key(
                original_decision,
                dot_separated_key='administrativeReview.reviewerTitle',
                new_value={'fi': 'administrativeReview.reviewerTitle'},
                missing_key_handler='skip'
            )
            # ---

            # Proposal
            update_inner_dictionary_key(
                original_decision,
                dot_separated_key='proposal.result',
                new_value='proposal.result',
                missing_key_handler='skip'
            )
            update_inner_dictionary_key(
                original_decision,
                dot_separated_key='proposal.presenterTitle',
                new_value={'fi': 'proposal.presenterTitle'},
                missing_key_handler='skip'
            )
            update_inner_dictionary_key(
                original_decision,
                dot_separated_key='proposal.rationale',
                new_value='proposal.rationale',
                missing_key_handler='skip'
            )
            # ---

            update_inner_dictionary_key(
                original_decision,
                dot_separated_key='appealInstructions',
                new_value='appealInstructions',
                missing_key_handler='skip'
            )
            update_inner_dictionary_key(
                original_decision,
                dot_separated_key='extensionInfo',
                new_value='extensionInfo',
                missing_key_handler='skip'
            )

        case _:
            raise Exception(f"Unknown decision type {decision_type}")

    return original_decision


_workflow_base_scrambling_keys = dict(
    id=None,
    documentState=None,
    state=None,
    code=None,
    lastHandlerPersonId=None,
    lastHandledTime=None,
    assignedHandlerId=None,
    creationTime=None,
    organisations=None,  # Cannot contain freeform text
    application=[
        lambda original_value: _handle_application_scrambling(
            original_value['application']
        )
    ],
    applicationHistory=[
        lambda original_value: [
            _handle_application_scrambling(history_entry)
            for history_entry in original_value['applicationHistory']
        ]
    ],
    decision=[
        lambda original_value: _handle_decision_scrambling(original_value['decision'])
    ],
    decisionHistory=[
        lambda original_value: [
            _handle_decision_scrambling(history_entry)
            for history_entry in original_value['decisionHistory']
        ]
    ],
    createdByPersonId=None,
    type=None,  # < datatype discriminator
    studentId=None,
    initiatorType=None,
    cancellingDisabled=None,
    mustPrintDecision=None,
    personFirstNames=[
        get_scrambled_first_name,
    ],
    personLastName=[
        get_scrambled_last_name,
    ],
    personStudentNumber=[
        (
            get_string_shuffled_with_mask,
            dict(old_value_key_getter_func=lambda x: x['personStudentNumber'])
        ),
    ],
    cancelReason=[
        lambda original_val: "cancelReason"
    ],
    cancelTime=None,
    cancellerId=None,
    cancelledByType=None,
    studyRightId=None,
)


# NOT VERIFIED
class CustomAttainmentWorkflowScrambler(SingletonMetaScrambler):
    # key=None means "Keep the original value"
    # lambda x: None means -> set the value None
    discriminator = 'CustomAttainmentWorkflow'
    scrambling_keys = _workflow_base_scrambling_keys | dict(
        plannedParentModuleId=None,
        degreeProgrammeId=None,
        degreeProgrammeGroupId=None,
        plannedCredits=None,
        name=[
            lambda original_val: "name"
        ],
        responsibleTeacher=[
            lambda original_val: "responsibleTeacher"
        ],
        applicationRationale=[
            lambda original_val: "applicationRationale"
        ],
        attainmentDescription=[
            lambda original_val: "attainmentDescription"
        ],
        customStudyDraft=[
            lambda original_val: update_inner_dictionary_key(
                original_val,
                dot_separated_key='customStudyDraft',
                new_value=_handle_custom_study_drafts,
                missing_key_handler='skip'
            ),
        ],
        attainmentLanguage=None,
        formalRecommendation=[
            (
                update_inner_dictionary_key,
                dict(
                    dot_separated_key='formalRecommendation.responsiblePerson',
                    new_value='formalRecommendation.responsiblePerson',
                    missing_key_handler='skip'
                )
            ),
            (
                update_inner_dictionary_key,
                dict(
                    dot_separated_key='formalRecommendation.responsiblePersonTitle',
                    new_value='formalRecommendation.responsiblePersonTitle',
                    missing_key_handler='skip'
                )
            ),
            (
                update_inner_dictionary_key,
                dict(
                    dot_separated_key='formalRecommendation.additionalInformation',
                    new_value='formalRecommendation.additionalInformation',
                    missing_key_handler='skip'
                )
            ),
            (
                update_inner_dictionary_key,
                dict(
                    dot_separated_key='formalRecommendation.comment',
                    new_value='formalRecommendation.comment',
                    missing_key_handler='skip'
                )
            ),
        ],
        contentRecommendation=[
            (
                update_inner_dictionary_key,
                dict(
                    dot_separated_key='contentRecommendation.responsiblePerson',
                    new_value='contentRecommendation.responsiblePerson',
                    missing_key_handler='skip'
                )
            ),
            (
                update_inner_dictionary_key,
                dict(
                    dot_separated_key='contentRecommendation.responsiblePersonTitle',
                    new_value='contentRecommendation.responsiblePersonTitle',
                    missing_key_handler='skip'
                )
            ),
            (
                update_inner_dictionary_key,
                dict(
                    dot_separated_key='contentRecommendation.additionalInformation',
                    new_value='contentRecommendation.additionalInformation',
                    missing_key_handler='skip'
                )
            ),
            (
                update_inner_dictionary_key,
                dict(
                    dot_separated_key='contentRecommendation.comment',
                    new_value='contentRecommendation.comment',
                    missing_key_handler='skip'
                )
            ),
        ],
        planId=None,
        moduleId=None,
        moduleGroupId=None,
        moduleContentWorkflow=None,
    )

    @classmethod
    def scramble(cls, entity: dict, processed_keys: set) -> dict:
        if entity['type'] != cls.discriminator:
            return entity

        return super().scramble(entity, processed_keys)


#  OK..?
class CustomModuleContentWorkflowScrambler(SingletonMetaScrambler):
    # key=None means "Keep the original value"
    # lambda x: None means -> set the value None
    discriminator = 'CustomModuleContentWorkflow'
    scrambling_keys = _workflow_base_scrambling_keys | dict(
        plannedParentModuleId=None,
        degreeProgrammeId=None,
        degreeProgrammeGroupId=None,
        plannedCredits=None,
        name=[
            lambda original_val: "name"
        ],
        responsibleTeacher=[
            lambda original_val: "responsibleTeacher"
        ],
        applicationRationale=[
            lambda original_val: "applicationRationale"
        ],
        attainmentDescription=[
            lambda original_val: "attainmentDescription"
        ],
        customStudyDrafts=[
            lambda original_val: update_inner_dictionary_key(
                original_val,
                dot_separated_key='customStudyDraft',
                new_value=_handle_custom_study_drafts,
                missing_key_handler='skip'
            ),
        ],
        attainmentLanguage=None,
        formalRecommendation=[
            (
                update_inner_dictionary_key,
                dict(
                    dot_separated_key='formalRecommendation.responsiblePerson',
                    new_value='formalRecommendation.responsiblePerson',
                    missing_key_handler='skip'
                )
            ),
            (
                update_inner_dictionary_key,
                dict(
                    dot_separated_key='formalRecommendation.responsiblePersonTitle',
                    new_value='formalRecommendation.responsiblePersonTitle',
                    missing_key_handler='skip'
                )
            ),
            (
                update_inner_dictionary_key,
                dict(
                    dot_separated_key='formalRecommendation.additionalInformation',
                    new_value='formalRecommendation.additionalInformation',
                    missing_key_handler='skip'
                )
            ),
            (
                update_inner_dictionary_key,
                dict(
                    dot_separated_key='formalRecommendation.comment',
                    new_value='formalRecommendation.comment',
                    missing_key_handler='skip'
                )
            ),
        ],
        contentRecommendation=[
            (
                update_inner_dictionary_key,
                dict(
                    dot_separated_key='contentRecommendation.responsiblePerson',
                    new_value='contentRecommendation.responsiblePerson',
                    missing_key_handler='skip'
                )
            ),
            (
                update_inner_dictionary_key,
                dict(
                    dot_separated_key='contentRecommendation.responsiblePersonTitle',
                    new_value='contentRecommendation.responsiblePersonTitle',
                    missing_key_handler='skip'
                )
            ),
            (
                update_inner_dictionary_key,
                dict(
                    dot_separated_key='contentRecommendation.additionalInformation',
                    new_value='contentRecommendation.additionalInformation',
                    missing_key_handler='skip'
                )
            ),
            (
                update_inner_dictionary_key,
                dict(
                    dot_separated_key='contentRecommendation.comment',
                    new_value='contentRecommendation.comment',
                    missing_key_handler='skip'
                )
            ),
        ],
        approvedModuleId=None,
        courseUnitSelections=None,
        moduleContentWorkflow=None,  #
        customCourseUnitAttainmentSelections=None,  #
        customModuleAttainmentSelections=None,  #
        parentModuleId=None,
        educationId=None,
        moduleSelections=None,
        originalReferredPlanId=None,
    )

    @classmethod
    def scramble(cls, entity: dict, processed_keys: set) -> dict:
        if entity['type'] != cls.discriminator:
            return entity

        return super().scramble(entity, processed_keys)


# NOT VERIFIED
class StudyRightExtensionWorkflowScrambler(SingletonMetaScrambler):
    # key=None means "Keep the original value"
    # lambda x: None means -> set the value None
    discriminator = 'StudyRightExtensionWorkflow'
    scrambling_keys = _workflow_base_scrambling_keys | dict(
        id=None,
        planId=None,
        planSnapshot=[
            lambda original_application: update_inner_dictionary_key(
                original_application,
                'planSnapshot.customStudyDrafts',
                new_value=_handle_custom_study_drafts,
                missing_key_handler='skip'
            ),
            lambda original_application: update_inner_dictionary_key(
                original_application,
                'planSnapshot.name',
                new_value='planSnapshot.name',
                missing_key_handler='skip'
            ),
            lambda original_application: update_inner_dictionary_key(
                original_application,
                'planSnapshot.timelineNotes',
                new_value='planSnapshot.timelineNotes',
                missing_key_handler='skip'
            ),
        ],
        educationId=None,
        studyRightValidity=None,
        previousExtensions=[
            lambda original_application: update_inner_dictionary_key(
                original_application,
                'previousExtensions.grantReason',
                new_value='previousExtensions.grantReason',
                missing_key_handler='skip',
            ),
            lambda original_application: update_inner_dictionary_key(
                original_application,
                'previousExtensions.deleteReason',
                new_value='previousExtensions.deleteReason',
                missing_key_handler='skip',
            )
        ],
        termRegistrations=None,  # Should be non-scrambleable
        usedAttendanceTerms=None,
        usedAbsenceTerms=None,
        usedStatutoryAbsenceTerms=None,
        termsWithoutRegistration=None,
        attainmentIds=None,
        phase1Progress=None,  # Seems benign
        phase2Progress=None,  # Seems benign
        requestedTerms=None,
        delayRationale=[
            lambda rationale: 'delayRationale' if rationale else rationale,
        ],
        applicationRationale=[
            lambda rationale: 'applicationRationale' if rationale else rationale,
        ],
        moduleContentWorkflow=None,
    )

    @classmethod
    def scramble(cls, entity: dict, processed_keys: set) -> dict:
        if entity['type'] != cls.discriminator:
            return entity

        return super().scramble(entity, processed_keys)


# OK...?
class PriorLearningInclusionWorkflowScrambler(SingletonMetaScrambler):
    # key=None means "Keep the original value"
    # lambda x: None means -> set the value None
    discriminator = 'PriorLearningInclusionWorkflow'
    scrambling_keys = _workflow_base_scrambling_keys | dict(
        id=None,
        priorLearnings=[
            lambda original_val: update_inner_dictionary_key(
                original_val,
                dot_separated_key='priorLearnings.name',
                new_value=(
                    scramble_with_weighted_pseudorandom,
                    dict(
                        key='name',
                        weights=[
                            ("Teknisen matematiikan kielikokeen kesäkurssi", 500),
                            ("Matematiikan alkeet Ipsum", 250),
                            ("Matematiikan alkeet ja väitöskirjan kirjoittaminen", 100),
                            ("Pallerojumppaamisen edut", 42),
                        ],
                        scramble_seed_key=lambda x: x['localId'],
                        scramble_empty_values=False,
                        missing_key_handler='skip'
                    )
                ),
                missing_key_handler='skip'
            ),
            lambda original_val: update_inner_dictionary_key(
                original_val,
                dot_separated_key='priorLearnings.organisation',
                new_value="organisation",
                missing_key_handler='skip'
            ),
            lambda original_val: update_inner_dictionary_key(
                original_val,
                dot_separated_key='priorLearnings.grade',
                new_value=(
                    scramble_with_weighted_pseudorandom,
                    dict(
                        key='grade',
                        weights=[
                            ("5", 100),
                            ("4", 250),
                            ("3", 500),
                            ("1", 350),
                        ],
                        scramble_seed_key=lambda x: x['localId'],
                        scramble_empty_values=False,
                        missing_key_handler='skip'
                    )
                ),
                missing_key_handler='skip'
            ),
            lambda original_val: update_inner_dictionary_key(
                original_val,
                dot_separated_key='priorLearnings.gradeScale',
                new_value='Grade scale 1-5',
                missing_key_handler='skip'
            ),
            lambda original_val: update_inner_dictionary_key(
                original_val,
                dot_separated_key='priorLearnings.credits',
                new_value=(
                    scramble_with_weighted_pseudorandom,
                    dict(
                        key='credits',
                        weights=[
                            ("30 op", 50),
                            ("15 op", 100),
                            ("5 op", 150),
                            ("5 ov", 25),
                            ("2 pallerojumppaa", 5),
                        ],
                        scramble_seed_key=lambda x: x['localId'],
                        scramble_empty_values=False,
                        missing_key_handler='skip'
                    )
                ),
                missing_key_handler='skip'
            ),
            lambda original_val: update_inner_dictionary_key(
                original_val,
                dot_separated_key='priorLearnings.description',
                new_value=(
                    scramble_with_weighted_pseudorandom,
                    dict(
                        key='description',
                        weights=[
                            ("Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat", 250),
                            ("Lorem ipsum dolor sit amet, consectetur adipiscing elit", 250),
                            ("15 pallerojumppaa ja Lorem Ipsum Dolores", 15),
                            ("1 pallerojumppa ja Lorem Ipsumit", 1),
                        ],
                        scramble_seed_key=lambda x: x['localId'],
                        scramble_empty_values=False,
                        missing_key_handler='skip'
                    )
                ),
                missing_key_handler='skip'
            ),
        ],
        name=[lambda x: "Name"],
        customStudyDraft=[
            lambda original_val: update_inner_dictionary_key(
                original_val,
                dot_separated_key='customStudyDraft',
                new_value=_handle_custom_study_drafts,
                missing_key_handler='skip'
            ),
        ],
        planId=None,
        formalRecommendation=None,
        moduleId=None,
        moduleGroupId=None,
        contentRecommendation=None,
        moduleContentWorkflow=None,  #
        degreeProgrammeId=None,
        degreeProgrammeGroupId=None,
        plannedParentModuleId=None,
    )

    @classmethod
    def scramble(cls, entity: dict, processed_keys: set) -> dict:
        if entity['type'] != cls.discriminator:
            return entity

        return super().scramble(entity, processed_keys)


# OK...?
class PriorLearningSubstitutionWorkflowScrambler(SingletonMetaScrambler):
    # key=None means "Keep the original value"
    # lambda x: None means -> set the value None
    discriminator = 'PriorLearningSubstitutionWorkflow'
    scrambling_keys = _workflow_base_scrambling_keys | dict(
        priorLearnings=[
            lambda original_val: update_inner_dictionary_key(
                original_val,
                dot_separated_key='priorLearnings.name',
                new_value=(
                    scramble_with_weighted_pseudorandom,
                    dict(
                        key='name',
                        weights=[
                            ("Teknisen matematiikan kielikokeen kesäkurssi", 500),
                            ("Matematiikan alkeet Ipsum", 250),
                            ("Matematiikan alkeet ja väitöskirjan kirjoittaminen", 100),
                            ("Pallerojumppaamisen edut", 42),
                        ],
                        scramble_seed_key=lambda x: x['localId'],
                        scramble_empty_values=False,
                        missing_key_handler='skip'
                    )
                ),
                missing_key_handler='skip'
            ),
            lambda original_val: update_inner_dictionary_key(
                original_val,
                dot_separated_key='priorLearnings.organisation',
                new_value="organisation",
                missing_key_handler='skip'
            ),
            lambda original_val: update_inner_dictionary_key(
                original_val,
                dot_separated_key='priorLearnings.grade',
                new_value=(
                    scramble_with_weighted_pseudorandom,
                    dict(
                        key='grade',
                        weights=[
                            ("5", 100),
                            ("4", 250),
                            ("3", 500),
                            ("1", 350),
                        ],
                        scramble_seed_key=lambda x: x['localId'],
                        scramble_empty_values=False,
                        missing_key_handler='skip'
                    )
                ),
                missing_key_handler='skip'
            ),
            lambda original_val: update_inner_dictionary_key(
                original_val,
                dot_separated_key='priorLearnings.gradeScale',
                new_value='Grade scale 1-5',
                missing_key_handler='skip'
            ),
            lambda original_val: update_inner_dictionary_key(
                original_val,
                dot_separated_key='priorLearnings.credits',
                new_value=(
                    scramble_with_weighted_pseudorandom,
                    dict(
                        key='credits',
                        weights=[
                            ("30 op", 50),
                            ("15 op", 100),
                            ("5 op", 150),
                            ("5 ov", 25),
                            ("2 pallerojumppaa", 5),
                        ],
                        scramble_seed_key=lambda x: x['localId'],
                        scramble_empty_values=False,
                        missing_key_handler='skip'
                    )
                ),
                missing_key_handler='skip'
            ),
            lambda original_val: update_inner_dictionary_key(
                original_val,
                dot_separated_key='priorLearnings.description',
                new_value=(
                    scramble_with_weighted_pseudorandom,
                    dict(
                        key='description',
                        weights=[
                            ("Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat", 250),
                            ("Lorem ipsum dolor sit amet, consectetur adipiscing elit", 250),
                            ("15 pallerojumppaa ja Lorem Ipsum Dolores", 15),
                            ("1 pallerojumppa ja Lorem Ipsumit", 1),
                        ],
                        scramble_seed_key=lambda x: x['localId'],
                        scramble_empty_values=False,
                        missing_key_handler='skip'
                    )
                ),
                missing_key_handler='skip'
            ),
        ],
        planId=None,
        contentRecommendation=None,
        formalRecommendation=None,
        courseUnitId=None,
        courseUnitGroupId=None,
        moduleContentWorkflow=None,
    )

    @classmethod
    def scramble(cls, entity: dict, processed_keys: set) -> dict:
        if entity['type'] != cls.discriminator:
            return entity

        return super().scramble(entity, processed_keys)


# OK....??
class ModuleAttainmentWorkflowScrambler(SingletonMetaScrambler):
    # key=None means "Keep the original value"
    # lambda x: None means -> set the value None
    discriminator = 'ModuleAttainmentWorkflow'
    scrambling_keys = _workflow_base_scrambling_keys | dict(
        planContent=[
            lambda original_val: update_inner_dictionary_key(
                original_val,
                'planContent.customStudyDrafts',
                new_value=_handle_custom_study_drafts,
                missing_key_handler='skip'
            )
        ],
        formalRecommendation=None,
        contentRecommendation=None,
        moduleId=None,
        moduleGroupId=None,
        moduleContentWorkflow=None,
        planId=None,
    )

    @classmethod
    def scramble(cls, entity: dict, processed_keys: set) -> dict:
        if entity['type'] != cls.discriminator:
            return entity

        return super().scramble(entity, processed_keys)


class RequiredModuleContentWorkflowScrambler(SingletonMetaScrambler):
    # key=None means "Keep the original value"
    # lambda x: None means -> set the value None
    discriminator = 'RequiredModuleContentWorkflow'
    scrambling_keys = _workflow_base_scrambling_keys | dict(
        formalRecommendation=None,
        contentRecommendation=None,
        moduleId=None,
        moduleGroupId=None,
        approvedModuleId=None,
        courseUnitSelections=None,
        customCourseUnitAttainmentSelections=None,
        educationId=None,
        originalReferredPlanId=None,
        parentModuleId=None,
        moduleContentWorkflow=None,
        planId=None,
        customStudyDrafts=[
            lambda original_val: update_inner_dictionary_key(
                original_val,
                dot_separated_key='customStudyDrafts',
                new_value=_handle_custom_study_drafts,
                missing_key_handler='skip'
            ),
        ],
        moduleSelections=None,
        customModuleAttainmentSelections=None,
        applicationRationale=[
            lambda original_val: "applicationRationale" if original_val else original_val
        ],
    )

    @classmethod
    def scramble(cls, entity: dict, processed_keys: set) -> dict:
        if entity['type'] != cls.discriminator:
            return entity

        return super().scramble(entity, processed_keys)


# OK....??
class DegreeProgrammeAttainmentWorkflowScrambler(SingletonMetaScrambler):
    # key=None means "Keep the original value"
    # lambda x: None means -> set the value None
    discriminator = 'DegreeProgrammeAttainmentWorkflow'
    scrambling_keys = _workflow_base_scrambling_keys | dict(
        planContent=[
            lambda original_val: update_inner_dictionary_key(
                original_val,
                'planContent.customStudyDrafts',
                new_value=_handle_custom_study_drafts,
                missing_key_handler='skip'
            )
        ],
        degreeDeliveryMethod=[
            lambda original_val: scramble_with_weighted_pseudorandom(
                original_val,
                'degreeDeliveryMethod',
                weights={'PICK_UP': 1337, 'DIGITAL_CERTIFICATE': 4242},
                scramble_seed_key=lambda x: x['id']
            )
        ],
        deliveryAddress=[lambda x: None],
        questionnaireAnswers=[
            lambda original_val: update_inner_dictionary_key(
                original_val,
                'questionnaireAnswers.question',
                new_value=(
                    scramble_with_weighted_pseudorandom,
                    dict(
                        key='question',
                        weights=[
                            ({'fi': 'Nautitko banaani', 'en': 'Do you like bananas'}, 500),
                            ({'fi': 'Haluatko avokaado', 'en': 'Would you like an avocado'}, 500),
                            ({'fi': 'Haluatko ostaa hampurilainen', 'en': 'Would you like to buy an amburger'}, 500),
                        ],
                        scramble_seed_key=lambda x: x['questionId'],
                        scramble_empty_values=False,
                        missing_key_handler='skip'
                    )
                ), missing_key_handler='skip'
            ),
            lambda original_val: update_inner_dictionary_key(
                original_val,
                'questionnaireAnswers.guidance',
                new_value=(
                    scramble_with_weighted_pseudorandom,
                    dict(
                        key='guidance',
                        weights=[
                            ({'fi': 'Tämä on <b>tärkeää</b> tietää.', 'en': 'This is <b>important</b> to know.'}, 500),
                            ({'fi': 'Pakollinen kysymys', 'en': 'This question is mandatory'}, 500),
                            ({'fi': 'Sinapilla?', 'en': 'With mustard?'}, 500),
                        ],
                        scramble_seed_key=lambda x: x['questionId'],
                        scramble_empty_values=False,
                        missing_key_handler='skip'
                    )
                ), missing_key_handler='skip'
            ),
            lambda original_val: update_inner_dictionary_key(
                original_val,
                'questionnaireAnswers.answer',
                new_value=(
                    scramble_with_weighted_pseudorandom,
                    dict(
                        key='answer',
                        weights=[
                            ('Jep', 500),
                            ('Voiko sen saada mukaan taskuun?', 500),
                            ('Haluan kaksi', 500),
                            ('WAT', 500),
                            ('Joo ei :blink:', 500),
                        ],
                        scramble_seed_key=lambda x: x['questionId'],
                        scramble_empty_values=False,
                        missing_key_handler='skip'
                    )
                ), missing_key_handler='skip'
            )
        ],
        additionalInfo=[lambda x: 'additionalInfo'],
        planId=None,
        moduleId=None,
        moduleGroupId=None,
        contentRecommendation=None,
        moduleContentWorkflow=None,  #
        formalRecommendation=None,
        newWorkflowId=None,
        joinsAlumniAssociation=None,
    )

    @classmethod
    def scramble(cls, entity: dict, processed_keys: set) -> dict:
        if entity['type'] != cls.discriminator:
            return entity

        return super().scramble(entity, processed_keys)


class WorkflowScramblerSelector(SingletonMetaScrambler):
    """
    Selects the correct scrambler by class name:
    - entity['type'] + 'Scrambler' is the expected class naming structure.
    """
    # key=None means "Keep the original value"
    # lambda x: None means -> set the value None
    scrambling_keys = {}
    logged_warnings = set()

    @classmethod
    def scramble(cls, entity: dict, processed_keys: set) -> dict:
        entity_type = entity['type']
        _scrambler = getattr(sys.modules[__name__], entity_type + 'Scrambler', None)
        if _scrambler is None:
            if entity_type not in cls.logged_warnings:
                cls.logged_warnings.add(entity_type)
                logger.critical("No scrambler found for class %s", entity_type)
            processed_keys |= {'id', 'type'}

            return dict(id=entity['id'], type=entity['type'], metadata=entity['metadata'])
        else:

            return _scrambler.scramble(entity, processed_keys)
