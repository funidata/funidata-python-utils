from typing import Annotated

from pydantic import Field, field_serializer

from .base import SisBase, CommonBase
from .common import (
    OTM_ID_REGEX_VALIDATED_STR,
    LocalizedString,
    LocalDateTimeRange,
    STRIPPED_STR,
    sis_code_urn_pattern,
)
from ..common_serializers import serialize_as_list


class CooperationNetworkLocation(CommonBase):
    organisationTkCode: str
    roleUrn: Annotated[
        STRIPPED_STR,
        Field(pattern=sis_code_urn_pattern('cooperation-network-organisation-role'))
    ]
    validityPeriod: LocalDateTimeRange


class CooperationNetwork(SisBase):
    id: OTM_ID_REGEX_VALIDATED_STR
    networkId: str
    name: LocalizedString
    abbreviation: str
    validityPeriod: LocalDateTimeRange
    organisations: list[CooperationNetworkLocation]

    @field_serializer('organisations')
    def organisations_as_list_from_set(self, val: list[CooperationNetworkLocation] | None, _info):
        serialized_list = serialize_as_list(val)
        return serialized_list
