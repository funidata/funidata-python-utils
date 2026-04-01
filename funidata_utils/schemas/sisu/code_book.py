from typing import Annotated, Literal

from pydantic import Field, field_serializer, conset, conlist

from funidata_utils.schemas.common_serializers import serialize_as_list
from funidata_utils.schemas.sisu import LocalizedString
from funidata_utils.schemas.sisu.base import SisBase
from funidata_utils.schemas.sisu.common import (
    STRIPPED_STR, sis_code_urn_pattern, SIS_MAX_VERY_LARGE_SET_SIZE, OTM_ID_REGEX_VALIDATED_STR,
    SIS_MAX_SMALL_SET_SIZE,
)


class Code(SisBase):
    name: LocalizedString
    shortName: LocalizedString | None
    urn: Annotated[STRIPPED_STR, Field(pattern=sis_code_urn_pattern('.+'))]
    parentUrn: Annotated[STRIPPED_STR, Field(pattern=sis_code_urn_pattern('.+'))] | None
    isLeafNode: bool | None
    universitySpecifier: str | None # Literal['HY', 'JYU', 'LUT', 'TUNI', 'AALTO', 'ARC', 'SHH'] | None but I really don't want to keep updating this...
    deprecated: bool | None
    exceptionalVirtaValue: str | None
    type: Literal['Code']

class CompetencyCode(Code):
    type: Literal['CompetencyCode']
    credits: int | None

class CountryCode(Code):
    type: Literal['CountryCode']
    numeric: str | None
    alpha2: str | None
    alpha3: str | None

class CodeBook(SisBase):
    documentState: Literal['ACTIVE', 'DRAFT', 'DELETED']
    urn: Annotated[STRIPPED_STR, Field(pattern=sis_code_urn_pattern('.+'))]
    codeBookType: Literal['COMMON', 'CUSTOM'] | None
    name: LocalizedString
    classificationScopeUrns: conset(Annotated[STRIPPED_STR, Field(pattern=sis_code_urn_pattern('classification-scope'))], max_length=SIS_MAX_SMALL_SET_SIZE) | None  # noqa
    universityOrgIds: conlist(OTM_ID_REGEX_VALIDATED_STR, max_length=1) | None  # noqa
    codeVisibility: Literal['ALWAYS_VISIBLE', 'HIDING_CODES_ALLOWED']
    codes: conset(Code | CompetencyCode | CountryCode, min_length=1, max_length=SIS_MAX_VERY_LARGE_SET_SIZE)  # noqa

    @field_serializer("classificationScopeUrns", "codes")
    def serialize_set_as_list(self, v, _info) -> list | None:
        serialized_list = serialize_as_list(v)
        return serialized_list