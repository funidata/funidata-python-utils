import datetime
from pydantic import BaseModel, Field, field_serializer, conset
from typing import Annotated, Literal

from .base import SisBase
from .common import OTM_ID_REGEX_VALIDATED_STR, STRIPPED_STR, SIS_MAX_MEDIUM_SET_SIZE, sis_code_urn_pattern
from ..common_serializers import serialize_as_list


class AssociatedStudy(BaseModel):
    description: str
    credits: int
    attainmentLocation: Annotated[STRIPPED_STR, Field(pattern=sis_code_urn_pattern('educational-institution'))]
    associatedDegree: str
    attainmentDate: datetime.date


class AttainedQualification(SisBase):
    id: OTM_ID_REGEX_VALIDATED_STR
    documentState: Literal['ACTIVE', 'DRAFT', 'DELETED']
    qualificationId: OTM_ID_REGEX_VALIDATED_STR
    personId: str = Field(description='PrivatePersonId')
    studyRightId: str
    moduleGroupId: OTM_ID_REGEX_VALIDATED_STR | None = None
    associatedStudies: list[AssociatedStudy] | None = None
    additionalInformation: str | None = None
    attainmentDate: datetime.date | None = None
    studyFieldUrn: Annotated[STRIPPED_STR | None, Field(pattern=sis_code_urn_pattern('study-field'))] = None
    attainmentMethod: Literal['AUTOMATIC', 'MANUAL'] = 'MANUAL'
    credits: int | None = None
    attainmentIds: conset(OTM_ID_REGEX_VALIDATED_STR, max_length=SIS_MAX_MEDIUM_SET_SIZE) | None = None # noqa
    childAttainedQualificationIds: conset(OTM_ID_REGEX_VALIDATED_STR, max_length=SIS_MAX_MEDIUM_SET_SIZE) | None = None # noqa
    registrationDate: datetime.date | None = None
    verifierPersonId: OTM_ID_REGEX_VALIDATED_STR | None = None

    @field_serializer("attainmentIds", "childAttainedQualificationIds")
    def serialize_set_as_list_str(self, v, _info) -> list[str] | None:
        serialized_list = serialize_as_list(v)
        return serialized_list
