#  Copyright (c) 2025 Funidata Oy.
#  All rights reserved.
# ------------------------------------------------------------------------------
import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, field_serializer, Field, BeforeValidator

from funidata_utils.schemas.sisu.base import HashableBaseModel, SisBase


SIS_MAX_VERY_LONG_STRING_LENGTH = 65000
SIS_MAX_LONG_STRING_LENGTH = 8000
SIS_MAX_MEDIUM_STRING_LENGTH = 1024
SIS_MAX_TERSE_STRING_LENGTH = 255
SIS_MAX_SHORT_STRING_LENGTH = 100

SIS_MAX_TWEET_LENGTH = 160

SIS_MAX_VERY_LARGE_SET_SIZE = 20000
SIS_MAX_BIG_SET_SIZE = 4000
SIS_MAX_MEDIUM_SET_SIZE = 200
SIS_MAX_SMALL_SET_SIZE = 20

OTM_ID_REGEX_PATTERN = '^([a-zA-Z]{2,5})-[A-Za-z0-9_\\-]{1,58}$'
OTM_ID_REGEX_VALIDATED_STR = Annotated[str, Field(pattern=OTM_ID_REGEX_PATTERN)]

STRIPPED_STR = Annotated[str, BeforeValidator(lambda x: str.strip(x) if isinstance(x, str) else x)]


def check_has_3_slashes(value):
    # TODO this is used in a case where Sisu expects the contents of a class in a "/" delimited str
    # we might want to rework this one day to actually validate the contents using a class
    if value.count('/') != 3:
        raise ValueError(
            'String did not contain 3 slashes: %s', value
        )
    return value


STRING_WITH_3_SLASHES = Annotated[STRIPPED_STR, BeforeValidator(check_has_3_slashes)]


def sis_code_urn_pattern(codebook: str):
    return f'^(urn:code:{codebook})(:[A-z_0-9-]+)*$'


class LocalDateRange(BaseModel):
    startDate: datetime.date | None = None
    endDate: datetime.date | None = None

    @field_serializer('startDate', 'endDate')
    def serialize_dt(self, dt: datetime.date | None, _info):
        if dt is None:
            return dt
        return dt.isoformat()


class LocalDateTimeRange(BaseModel):
    startDateTime: datetime.datetime | None = None
    endDateTime: datetime.datetime | None = None

    @field_serializer('startDateTime', 'endDateTime')
    def serialize_dt(self, dt: datetime.datetime | None, _info):
        if dt is None:
            return dt
        return dt.isoformat()


class CreditRange(BaseModel):
    min: float
    max: float | None = None


class LocalizedString(HashableBaseModel):
    fi: str | None = None
    en: str | None = None
    sv: str | None = None


class OrganisationRoleShareBase(HashableBaseModel):
    organisationId: OTM_ID_REGEX_VALIDATED_STR | None
    educationalInstitutionUrn: Annotated[STRIPPED_STR | None, Field(pattern=sis_code_urn_pattern('educational-institution'))] = None
    roleUrn: Annotated[STRIPPED_STR, Field(pattern=sis_code_urn_pattern('organisation-role'))]
    share: Annotated[float, Field(strict=False, ge=0, le=1)]


class OrganisationRoleShare(OrganisationRoleShareBase):
    validityPeriod: LocalDateRange | None


class FinnishAddress(BaseModel):
    countryUrn: Annotated[STRIPPED_STR, Field(pattern=sis_code_urn_pattern('country'))]
    isUserEditable: bool
    type: str = 'FinnishAddress'
    streetAddress: str | None = None
    postalCode: str | None = None
    city: str | None = None


class GenericAddress(BaseModel):
    countryUrn: Annotated[STRIPPED_STR, Field(pattern=sis_code_urn_pattern('country'))]
    isUserEditable: bool
    type: str = 'GenericAddress'
    address: str | None = None


class PersonWithModuleResponsibilityInfoType(BaseModel):
    text: LocalizedString | None = None
    personId: OTM_ID_REGEX_VALIDATED_STR | None = None
    roleUrn: Literal[
        'urn:code:module-responsibility-info-type:responsible-teacher',
        'urn:code:module-responsibility-info-type:administrative-person',
        'urn:code:module-responsibility-info-type:contact-info',
    ]
    validity: LocalDateRange | None = None
    validityPeriod: LocalDateRange | None = None
