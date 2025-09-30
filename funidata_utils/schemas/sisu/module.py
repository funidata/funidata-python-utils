#  Copyright (c) 2025 Funidata Oy.
#  All rights reserved.
# ------------------------------------------------------------------------------
import datetime
from typing import Literal, Annotated, Self, Any, Union, get_args, TYPE_CHECKING

from pydantic import BaseModel, Field, field_serializer, Tag, Discriminator, conset, ConfigDict, TypeAdapter, model_validator

from .common import (
    SIS_MAX_LONG_STRING_LENGTH,
    OTM_ID_REGEX_PATTERN,
    SIS_MAX_TERSE_STRING_LENGTH,
    LocalDateRange,
    LocalizedString, CreditRange, sis_code_urn_pattern,
    OrganisationRoleShareBase,
    STRIPPED_STR, SIS_MAX_MEDIUM_SET_SIZE, SIS_MAX_SMALL_SET_SIZE,
)


class Rule(BaseModel):
    model_config = ConfigDict(extra='allow')
    
    localId: str


class Module(BaseModel):
    model_config = ConfigDict(extra='allow')
    documentState: Literal['ACTIVE', 'DRAFT', 'DELETED']
    type: Literal[
        'StudyModule',
        'GroupingModule',
        'DegreeProgramme'
    ]

    metadata: dict = Field(exclude=True)
    groupId: Annotated[str, OTM_ID_REGEX_PATTERN]

    name: LocalizedString
    rule: Rule
    moduleContentApprovalRequired: bool


class StudyModule(Module):
    type: Literal['StudyModule']
    abbreviation: str | None = None
    tweetText: LocalizedString | None = None
    outcomes: LocalizedString | None = None
    prerequisites: LocalizedString | None = None
    substitutions: LocalizedString | None = None
    searchTags: conset(str, max_length=SIS_MAX_MEDIUM_SET_SIZE) | None = None
    studyLevel: Annotated[STRIPPED_STR | None, Field(pattern=sis_code_urn_pattern('study-level'))]
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

    @model_validator(mode='after')
    def document_state_active_validators(self):
        if self.documentState != 'ACTIVE':
            return self

        if self.studyFields is None:
            raise ValueError("StudyField may not be null on documentState ACTIVE")

        if self.studyLevel is None:
            raise ValueError("StudyField may not be null on documentState ACTIVE")

        return self

    @field_serializer('searchTags', 'possibleAttainmentLanguages', 'studyFields')
    def sets_as_lists(self, v):
        if v is None:
            return None

        return list(v)


class DegreeProgramme(Module):
    type: Literal['DegreeProgramme']


class GroupingModule(Module):
    type: Literal['GroupingModule']


module = Annotated[Union[DegreeProgramme, StudyModule, GroupingModule], Field(discriminator='type')]
ModuleTypeAdapter = TypeAdapter(module)
