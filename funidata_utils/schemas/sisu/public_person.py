#  Copyright (c) 2025 Funidata Oy.
#  All rights reserved.
# ------------------------------------------------------------------------------
from pydantic import BaseModel, conlist

from .common import LocalizedString, OTM_ID_REGEX_VALIDATED_STR, SIS_MAX_SMALL_SET_SIZE

class PublicPerson(BaseModel):
    id: str = None
    universityOrgIds: conlist(OTM_ID_REGEX_VALIDATED_STR, max_length=SIS_MAX_SMALL_SET_SIZE)
    titles: LocalizedString | None = None
    firstName: str | None = None
    lastName: str | None = None
    emailAddress: str | None = None
