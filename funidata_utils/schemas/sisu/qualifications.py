#  Copyright (c) 2025 Funidata Oy.
#  All rights reserved.
# ------------------------------------------------------------------------------
import datetime
from typing import Literal, Annotated

from pydantic import BaseModel, Field, field_serializer

from .common import LocalizedString, sis_code_urn_pattern


class Qualifications(BaseModel):
    id: str
    documentState: Literal['ACTIVE', 'DRAFT', 'DELETED']
    universityOrgId: str
    type: Literal['FORMAL', 'CUSTOM', 'COMPETENCY']
    name: LocalizedString
    printName: LocalizedString | None = None
    code: str
    qualificationUrn: Annotated[str, Field(pattern=sis_code_urn_pattern('qualification'))]  # TODO: Verify
    competencyUrn: Annotated[str, Field(pattern=sis_code_urn_pattern('competency'))]
    requirementCollections: list[dict]  # TODO: RequirementCollection
    includeCompetencies: bool | None = None
    diplomaAppendix: LocalizedString | None = None
    instructions: LocalizedString | None = None
    state: Literal['NOT_READY', 'PUBLISHED', 'ARCHIVED']
    publishedOn: datetime.datetime
    customQualificationTypeUrn: Annotated[str, Field(pattern=sis_code_urn_pattern('custom-qualification-type'))]
    studyFieldUrn: Annotated[str, Field(pattern=sis_code_urn_pattern('study-field'))]

    @field_serializer('publishedOn')
    def serialize_dt(self, val: datetime.datetime | None, _info):
        if val is None:
            return None

        return val.strftime("%Y-%m-%dT%H:%M:%S")
