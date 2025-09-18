#  Copyright (c) 2025 Funidata Oy.
#  All rights reserved.
# ------------------------------------------------------------------------------

import datetime
from typing import Literal, Annotated

from pydantic import BaseModel, Field, field_serializer, conset

from .common import sis_code_urn_pattern, STRIPPED_STR, LocalizedString, OTM_ID_REGEX_VALIDATED_STR, SIS_MAX_SMALL_SET_SIZE


class CooperationNetworkIdentifiers(BaseModel):
    direction: Literal['INBOUND', 'OUTBOUND', 'NONE']
    organisationTkCode: Annotated[str, Field(min_length=1)]


class Organisation(BaseModel):
    id: OTM_ID_REGEX_VALIDATED_STR
    documentState: Literal['ACTIVE', 'DRAFT', 'DELETED']
    snapshotDateTime: datetime.datetime
    universityOrgId: OTM_ID_REGEX_VALIDATED_STR
    parentId: OTM_ID_REGEX_VALIDATED_STR | None = None
    predecessorIds: conset(OTM_ID_REGEX_VALIDATED_STR, max_length=SIS_MAX_SMALL_SET_SIZE)
    code: Annotated[str, Field(min_length=1)]
    name: LocalizedString
    abbreviation: LocalizedString | None = None
    status: Literal['ACTIVE', 'INACTIVE']
    educationalInstitutionUrn: Annotated[STRIPPED_STR | None, Field(pattern=sis_code_urn_pattern('educational-institution'))] = None
    cooperationNetworkIdentifiers: CooperationNetworkIdentifiers | None = None

    @field_serializer('snapshotDateTime')
    def serialize_ssdt(self, ssdt: datetime.datetime | None, _info):
        if ssdt is None:
            return None

        return ssdt.strftime("%Y-%m-%dT%H:%M:%S")

    @field_serializer('predecessorIds')
    def serialize_predecessor_ids(self, set_val: set[str], _info):
        return list(set_val)
