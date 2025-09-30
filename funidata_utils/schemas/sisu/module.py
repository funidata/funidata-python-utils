#  Copyright (c) 2025 Funidata Oy.
#  All rights reserved.
# ------------------------------------------------------------------------------
from typing import Literal, Annotated, Self, Any, Union

from pydantic import BaseModel, Field, field_serializer, conset, ConfigDict, TypeAdapter, model_validator, ValidationError

from .common import (
    OTM_ID_REGEX_PATTERN,
    LocalizedString, sis_code_urn_pattern,
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

    @model_validator(mode='wrap')
    @classmethod
    def handle_document_state_validations(cls, data, handler) -> Self:
        """
            Currently attempts to validate the class using the default validation handlers -
            If an error occurs and the object is not ACTIVE - it will return a model_construct'ed version of the class
        """
        try:
            return handler(data)
        except ValidationError as e:
            if data['documentState'] != 'ACTIVE':
                return cls.model_construct(**data)

            raise e


class StudyModule(Module):
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
