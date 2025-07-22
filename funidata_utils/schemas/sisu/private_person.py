#  Copyright (c) 2025 Funidata Oy.
#  All rights reserved.
# ------------------------------------------------------------------------------

import datetime
from typing import Literal
from pydantic import BaseModel, field_serializer, Field, constr, conset


CountryUrnStr = constr(pattern='(urn:code:country)(:[A-z_0-9]+)*')
SchoolEducationLangUrnStr = constr(pattern='(urn:code:school-education-language)(:[A-z_0-9]+)*')


class FinnishAddress(BaseModel):
    countryUrn: CountryUrnStr
    isUserEditable: bool
    type: str = 'FinnishAddress'
    streetAddress: str | None = None
    postalCode: str | None = None
    city: str | None = None


class GenericAddress(BaseModel):
    countryUrn: CountryUrnStr
    isUserEditable: bool
    type: str = 'GenericAddress'
    address: str | None = None


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
    username: str | None = None
    eduPersonPrincipalName: str | None = None
    employeeNumber: str | None = None
    phoneNumber: str | None = None
    primaryEmail: str | None = None
    secondaryEmail: str | None = None
    primaryAddress: FinnishAddress | None = None
    secondaryAddress: FinnishAddress | GenericAddress | None = None
    genderUrn: constr(pattern='(urn:code:gender)(:[A-z_0-9]+)*')
    citizenshipUrns: conset(CountryUrnStr, min_length=1) | None = None
    motherTongueUrn: constr(pattern='(urn:code:language)(:[A-z_0-9]+)*') | None = None
    preferredLanguageUrn: constr(pattern='(urn:code:preferred-language)(:[A-z_0-9]+)*') | None = None
    schoolEducationLanguageUrns: conset(SchoolEducationLangUrnStr, min_length=1) | None = None
    municipalityUrn: constr(pattern='(urn:code:municipality)(:[A-z_0-9]+)*') | None = None
    oppijanumero: str | None = None
    oids: list[str] = []
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
        if not val:
            return None
        return list(val)
