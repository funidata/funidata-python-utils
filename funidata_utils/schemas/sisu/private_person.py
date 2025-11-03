#  Copyright (c) 2025 Funidata Oy.
#  All rights reserved.
# ------------------------------------------------------------------------------

import datetime
from typing import Literal, Annotated

from pydantic import BaseModel, field_serializer, conset, Field, AfterValidator, AliasChoices

from .common import FinnishAddress, GenericAddress, STRIPPED_STR, sis_code_urn_pattern
from ..common_serializers import serialize_as_list


CountryUrnStr = Annotated[STRIPPED_STR, Field(pattern=sis_code_urn_pattern('country'))]
SchoolEducationLangUrnStr = Annotated[STRIPPED_STR, Field(pattern=sis_code_urn_pattern('school-education-language'))]

OID_REGEX_PATTERN = '^1\.2\.246\.562\.(?:24|98)\.[1-9][0-9]{10}$'

def calculate_oid_luhn_checksum(digits: list[int]) -> int:
    return 10 - ((sum(digits[0::2]) + sum(sum(divmod(d * 2, 10)) for d in digits[1::2])) % 10) % 10

def calculate_oid_ibm_checksum(digits: list[int]) -> int:
    checksum=0
    weights=[7, 3, 1]

    for i, numericValue in enumerate(reversed(digits)):
        weight = weights[i % len(weights)]
        checksum += numericValue * weight

    return (10 - (checksum % 10)) % 10

def oid_validator(oid: str) -> str:
    split_oid = oid.split('.')
    last_digits = [int(ch) for ch in split_oid[-1]]
    check_digit = last_digits[-1]
    digits = last_digits[:-1]

    match split_oid[-2]:
        case '98':
            if check_digit != calculate_oid_luhn_checksum(digits):
                raise ValueError('OID is not luhn valid')
        case '24':
            if check_digit != calculate_oid_ibm_checksum(digits):
                raise ValueError('OID is not ibm valid')
        case _:
            raise ValueError('OID tree space is not valid')
    return oid

OID_STR = Annotated[str, Field(pattern=OID_REGEX_PATTERN), AfterValidator(oid_validator)]

class ClassifiedPersonInfo(BaseModel):
    isPhoneNumberClassified: bool | None = None
    isSecondaryEmailClassified: bool | None = None
    isPrimaryAddressClassified: bool | None = None
    isSecondaryAddressClassified: bool | None = None
    isMunicipalityUrnClassified: bool | None = None
    changedById: str | None = None
    changedOn: datetime.date | None = None

    @field_serializer('changedOn')
    def date_as_isoformat(self, val: datetime.date | None, _info):
        if val is None:
            return None

        return val.isoformat()


class PrivatePerson(BaseModel):
    id: str = None
    studentNumber: str | None = None
    personalIdentityCode: str | None = None
    finnAuthId: str | None = None
    eidasId: str | None = None
    dateOfBirth: datetime.date | None = None
    firstNames: str | None = None
    callName: str | None = None
    lastName: str | None = None
    userName: str | None = Field(validation_alias=AliasChoices('userName', 'username'), default=None)
    eduPersonPrincipalName: str | None = None
    employeeNumber: str | None = None
    phoneNumber: str | None = None
    primaryEmail: str | None = None
    secondaryEmail: str | None = None
    primaryAddress: FinnishAddress | None = None
    secondaryAddress: FinnishAddress | GenericAddress | None = None
    genderUrn: Annotated[STRIPPED_STR, Field(pattern=sis_code_urn_pattern('gender'))]
    citizenshipUrns: set[CountryUrnStr] | None = None
    motherTongueUrn: Annotated[STRIPPED_STR | None, Field(pattern=sis_code_urn_pattern('language'))] = None
    preferredLanguageUrn: Annotated[STRIPPED_STR | None, Field(pattern=sis_code_urn_pattern('preferred-language'))] = None
    schoolEducationLanguageUrns: conset(SchoolEducationLangUrnStr, min_length=1) | None = None
    municipalityUrn: Annotated[STRIPPED_STR | None, Field(pattern=sis_code_urn_pattern('municipality'))] = None
    oppijanumero: str | None = None
    oids: list[OID_STR] = []
    dead: bool = False
    classifiedPersonInfo: ClassifiedPersonInfo | None = None
    personalDataSafetyNonDisclosure: bool | None = None
    studentStatus: Literal['ACTIVE', 'NONE']
    employeeStatus: Literal['ACTIVE', 'NONE', 'INACTIVE']
    identityConfirmed: bool = True
    secondOfficialLanguageStudyObligation: Literal['EXEMPTION_GRANTED', 'OBLIGATED'] | None = None
    documentState: Literal['ACTIVE', 'DRAFT', 'DELETED']

    @field_serializer('dateOfBirth')
    def date_as_isoformat(self, val: datetime.date | None, _info):
        if val is None:
            return None

        return val.isoformat()

    @field_serializer('citizenshipUrns', 'schoolEducationLanguageUrns')
    def set_of_strings_as_list(self, val: set[str] | None, _info):
        serialized_list = serialize_as_list(val)
        return serialized_list
