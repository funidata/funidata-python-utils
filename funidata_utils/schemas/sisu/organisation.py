#  Copyright (c) 2025 Funidata Oy.
#  All rights reserved.
# ------------------------------------------------------------------------------

import datetime
from typing import Literal, Annotated

from pydantic import BaseModel, Field, field_serializer

from .common import sis_code_urn_pattern, STRIPPED_STR, LocalizedString, OTM_ID_REGEX_VALIDATED_STR


class CooperationNetworkIdentifiers(BaseModel):
    direction: Literal['INBOUND', 'OUTBOUND', 'NONE']
    organisationTkCode: Annotated[str, Field(min_length=1)]


class Organisation(BaseModel):
    id: OTM_ID_REGEX_VALIDATED_STR
    documentState: Literal['ACTIVE', 'DRAFT', 'DELETED']
    snapshotDateTime: datetime.datetime
    universityOrgId: Annotated[str, Field(min_length=1)]
    parentId: str | None = None
    predecessorIds: list[str]
    code: Annotated[str, Field(min_length=1)]
    name: LocalizedString
    abbreviation: LocalizedString | None = None
    status: Literal['ACTIVE', 'INACTIVE']
    educationalInstitutionUrn: Annotated[STRIPPED_STR, Field(pattern=sis_code_urn_pattern('educational-institution'))] | None = None
    cooperationNetworkIdentifiers: CooperationNetworkIdentifiers | None = None

    @field_serializer('snapshotDateTime')
    def serialize_ssdt(self, ssdt: datetime.datetime | None, _info):
        if ssdt is None:
            return None

        return ssdt.strftime("%Y-%m-%dT%H:%M:%S")
