import copy

import pytest

from funidata_utils.data_scramblers.private_person import PrivatePersonScrambler


@pytest.mark.unit
def test_private_person_scrambler_scrambles_keys():
    data = {
        "documentState": "DRAFT",
        "id": "otm-123456",
        "studentNumber": "string",
        "personalIdentityCode": "string",
        "finnAuthId": "1234567892",
        "eidasId": "string",
        "dateOfBirth": "2026-09-14",
        "userName": "string",
        "eduPersonPrincipalName": "string",
        "employeeNumber": "string",
        "phoneNumber": "string",
        "primaryAddress": {
            "countryUrn": "urn:code:country:*",
            "isUserEditable": True,
            "type": "FinnishAddress",
            "streetAddress": "string",
            "postalCode": "string",
            "city": "string"
        },
        "secondaryAddress": {
            "countryUrn": "urn:code:country:*",
            "isUserEditable": True,
            "type": "string",
            "streetAddress": "string",
            "postalCode": "string",
            "city": "string"
        },
        "genderUrn": "urn:code:gender:*",
        "citizenshipUrns": [
            "urn:code:country:247",
            "urn:code:country:248"
        ],
        "motherTongueUrn": "urn:code:language:*",
        "preferredLanguageUrn": "urn:code:preferred-language:*",
        "schoolEducationLanguageUrns": [
            "urn:code:school-education-language:*"
        ],
        "municipalityUrn": "urn:code:municipality:*",
        "oppijanumero": "string",
        "oids": [
            "string"
        ],
        "dead": True,
        "classifiedPersonInfo": {
            "isPhoneNumberClassified": True,
            "isSecondaryEmailClassified": True,
            "isPrimaryAddressClassified": True,
            "isSecondaryAddressClassified": True,
            "isMunicipalityUrnClassified": True,
            "changedById": "otm-123456",
            "changedOn": "2026-09-14T09:25:06.091Z"
        },
        "personalDataSafetyNonDisclosure": True,
        "studentStatus": "ACTIVE",
        "employeeStatus": "ACTIVE",
        "identityConfirmed": True,
        "secondOfficialLanguageStudyObligation": "EXEMPTION_GRANTED",
        "graduationSurveyExemptionGranted": True,
        "mergedPersonId": "string",
        "loginDisabledType": "DISCIPLINARY",
        "firstNames": "string",
        "callName": "string",
        "lastName": "string",
        "primaryEmail": "string",
        "secondaryEmail": "string"
    }

    scrambled_data = PrivatePersonScrambler.scramble(copy.deepcopy(data), set())
    for key, _ in PrivatePersonScrambler.dict_items_with_scrambling():
        if key in {'oppijaID'}:
            # Keys deprecated, just check it is nulled
            assert scrambled_data.get(key) is None
        else:
            if isinstance(scrambled_data.get(key), bool):
                # Cannot reliably test for bool 50/50 changes
                continue

            assert scrambled_data.get(key, -42) != data.get(key, -42)
