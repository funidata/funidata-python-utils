from typing import Literal

from pydantic import BaseModel

from .common import LocalDateRange, LocalizedString


class CooperationNetworkStatus(BaseModel):
    direction: Literal["INBOUND", "OUTBOUND", "NONE"]
    organisationTkCode: str | None = None
    outboundStatus: Literal["NOT_VALID", "FORWARDED", "RECORDED", "REJECTED"] | None = None
    rejectionReason: LocalizedString | None = None
    outboundStatusMessage: str | None = None
    cooperationNetworkId: str | None = None
    universityOrgId: str | None = None
    homeStudyRightId: str | None = None
    inboundStatus: Literal["ACCEPTED", "PROCESSING", "REJECTED"] | None = None
    homeStudyRightValidity: LocalDateRange | None = None
