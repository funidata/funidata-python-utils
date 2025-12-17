#  Copyright (c) 2025 Funidata Oy.
#  All rights reserved.
# ------------------------------------------------------------------------------
from typing import Literal, Annotated, Any, Union

from pydantic import BaseModel, Field, field_serializer, conset, ConfigDict, TypeAdapter

from .base import SisBase
from .common import (
    OTM_ID_REGEX_PATTERN,
    LocalizedString, sis_code_urn_pattern,
    STRIPPED_STR, SIS_MAX_MEDIUM_SET_SIZE, SIS_MAX_SMALL_SET_SIZE, SIS_MAX_SHORT_STRING_LENGTH, CreditRange, LocalDateRange,
)
from ..common_serializers import serialize_as_list


class Rule(BaseModel):
    """WIP Class representing a SISU Rule object.
    Fields and validations are not complete yet
    """

    model_config = ConfigDict(extra='allow', from_attributes=True)

    localId: str


class Module(SisBase):
    """WIP Class representing a SISU module.
    Fields and validations are not complete yet
    """
    model_config = ConfigDict(extra='allow', from_attributes=True)
    documentState: Literal['ACTIVE', 'DRAFT', 'DELETED']
    type: Literal[
        'StudyModule',
        'GroupingModule',
        'DegreeProgramme'
    ]
    id: Annotated[str, OTM_ID_REGEX_PATTERN]
    groupId: Annotated[str, OTM_ID_REGEX_PATTERN]
    name: LocalizedString
    rule: Rule
    moduleContentApprovalRequired: bool


class DPSMBase(Module):
    """WIP Class representing a SISU DPSMBase object.
    Fields and validations are not complete yet"""

    code: Annotated[str, Field(min_length=1, max_length=SIS_MAX_SHORT_STRING_LENGTH)]
    targetCredits: CreditRange
    curriculumPeriodIds: conset(str, min_length=1, max_length=SIS_MAX_MEDIUM_SET_SIZE)
    approvalState: str  # TODO - enum
    validityPeriod: LocalDateRange

    @field_serializer('curriculumPeriodIds')
    def sets_as_list(self, v, _info) -> list[dict]:
        serialized_list = serialize_as_list(v)
        return serialized_list


class StudyModule(DPSMBase):
    """WIP Class representing a SISU StudyModule object.
    Fields and validations are not complete yet"""

    type: Literal['StudyModule']
    abbreviation: str | None = None
    tweetText: LocalizedString | None = None
    outcomes: LocalizedString | None = None
    prerequisites: LocalizedString | None = None
    substitutions: LocalizedString | None = None
    searchTags: conset(str, max_length=SIS_MAX_MEDIUM_SET_SIZE) | None = None
    studyLevel: Annotated[STRIPPED_STR, Field(pattern=sis_code_urn_pattern('study-level'))]
    possibleAttainmentLanguages: conset(
        Annotated[STRIPPED_STR, Field(pattern=sis_code_urn_pattern('official-language'))],
        max_length=SIS_MAX_SMALL_SET_SIZE
    ) | None = None
    studyFields: conset(
        Annotated[STRIPPED_STR, Field(pattern=sis_code_urn_pattern('study-field'))],
        max_length=SIS_MAX_SMALL_SET_SIZE
    ) | None
    graded: bool = True
    gradeScaleId: str | None = None
    customCodeUrns: Annotated[dict[str, list[str]] | None, Field(min_length=1)] = None
    contentFilter: Any

    @field_serializer('searchTags', 'possibleAttainmentLanguages', 'studyFields')
    def sets_as_lists(self, v):
        serialized_list = serialize_as_list(v)
        return serialized_list


class DegreeProgramme(DPSMBase):
    """WIP Class representing a SISU degree programme.
    Fields and validations are not complete yet
    """
    type: Literal['DegreeProgramme']


class GroupingModule(Module):
    """WIP Class representing a SISU grouping module.
    Fields and validations are not complete yet
    """
    type: Literal['GroupingModule']


module = Annotated[Union[DegreeProgramme, StudyModule, GroupingModule], Field(discriminator='type')]
ModuleTypeAdapter = TypeAdapter(module)
