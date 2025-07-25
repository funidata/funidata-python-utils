#  Copyright (c) 2025 Funidata Oy.
#  All rights reserved.
# ------------------------------------------------------------------------------

from typing import Literal, Annotated

from pydantic import BaseModel, Field

from .common import sis_code_urn_pattern, STRIPPED_STR, LocalizedString


class CooperationNetworkIdentifiers(BaseModel):
    direction: Literal['INBOUND', 'OUTBOUND', 'NONE']
    organisationTkCode: str

class Organisation(BaseModel):
    id: str
    documentState: Literal['ACTIVE', 'DRAFT', 'DELETED']
    snapshotDateTime: datetime.date
    universityOrgId: str
    parentId: str | None = None
    predecessorIds: list[str]
    code: str
    name: LocalizedString
    abbreviation: LocalizedString | None = None
    status: Literal['ACTIVE', 'INACTIVE']
    educationalInstitutionUrn: Annotated[STRIPPED_STR, Field(pattern=sis_code_urn_pattern('educational-institution'))] | None = None
    cooperationNetworkIdentifiers: CooperationNetworkIdentifiers | None = None

    @field_serializer('snapshotDateTime')
    def date_as_isoformat(self, val: datetime.date, _info):
        return val.isoformat()
