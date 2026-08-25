from typing import Tuple

from .replacement_data import first_names, last_names
from .utils.generic_scrambling import (
    replace_from_list, scramble_with_weighted_pseudorandom, hashlib_hash, random_shuffle, get_random_date,
)
from .utils.key_scramblers import (
    get_scrambled_first_name, get_scrambled_last_name, get_scrambled_nationalities, get_phone_number_shuffled_with_mask,
    get_scrambled_email,
)
from ..scramblers.base import SingletonMetaScrambler


class PrivatePersonScrambler(SingletonMetaScrambler):
    @classmethod
    def scramble(cls, entity: dict) -> dict:
        """ Only allow returning keys that have been verified to be scramble-able or non-scrambleable!"""
        _out_entity = {}

        # key=None means "Keep the original value"
        # lambda x: None means -> set the value None
        scrambling_keys = dict(
            id=None,
            documentState=None,
            studentNumber=[
                lambda x: None
            ],
            personalIdentityCode=[
                lambda x: None
            ],
            finnAuthId=[
                lambda x: None
            ],
            eidasId=[
                lambda x: None
            ],
            dateOfBirth=[
                (get_random_date, dict(n=entity['id']))
            ],
            firstNames=[
                get_scrambled_first_name
            ],
            callName=[
                get_scrambled_first_name
            ],
            lastName=[
                get_scrambled_last_name
            ],
            userName=[
                lambda x: None
            ],
            eduPersonPrinicpalName=[
                lambda x: f"{x['id']}@eppn.fi"
            ],
            employeeNumber=[
                (hashlib_hash, dict(key=entity.get('employeeNumber'), hash_function='sha256', output_length=67, return_int=False))
            ],
            phoneNumber=[
                get_phone_number_shuffled_with_mask
            ],
            primaryEmail=[
                get_scrambled_email
            ],
            secondaryEmail=[
                lambda x: None
            ],
            primaryAddress=[
                lambda x: dict(
                    countryUrn='urn:code:country:246',
                    type='FinnishAddress',
                    streetAddress='Hiomotie 32',
                    postalCode='00002',
                    city='Helsinki'
                )
            ],
            secondaryAddress=[
                lambda x: None
            ],
            genderUrn=[
                (
                    scramble_with_weighted_pseudorandom,
                    dict(
                        key='genderUrn',
                        weights={
                            'urn:code:gender:male': 5000,
                            'urn:code:gender:female': 5000,
                            'urn:code:gender:other': 250,
                            'urn:code:gender:not-known': 100,
                        },
                        scramble_seed_key=entity['id']
                    )
                )
            ],
            citizenshipUrns=[
                get_scrambled_nationalities
            ],
            motherTongueUrn=[
                (
                    scramble_with_weighted_pseudorandom,
                    dict(
                        key='motherTongueUrn',
                        weights={
                            'urn:code:language:fi': 5000,
                            'urn:code:language:sv': 250,
                            'urn:code:language:en': 50,
                        },
                        scramble_seed_key=entity['id']
                    )
                )
            ],
            preferredLanguageUrn=[
                (
                    scramble_with_weighted_pseudorandom,
                    dict(
                        key='preferredLanguageUrn',
                        weights={
                            'urn:code:language:fi': 5000,
                            'urn:code:language:sv': 250,
                            'urn:code:language:en': 50,
                        },
                        scramble_seed_key=entity['id']
                    )
                )
            ],
            schoolEducationLanguageUrns=[
                (
                    scramble_with_weighted_pseudorandom,
                    dict(
                        key='preferredLanguageUrn',
                        weights={
                            'urn:code:school-education-language:fi': 5000,
                            'urn:code:school-education-language:sv': 1000,
                            'urn:code:school-education-language:se': 50,
                            'urn:code:school-education-language:de': 50,
                            'urn:code:school-education-language:ru': 50,
                            'urn:code:school-education-language:en': 50,
                        },
                        scramble_seed_key=entity['id']
                    )
                )
            ],
            municipalityUrn=[
                (
                    scramble_with_weighted_pseudorandom,
                    dict(
                        key='municipalityUrn',
                        weights={
                            'urn:code:municipality:020': 1000,
                            'urn:code:municipality:091': 1000,
                            'urn:code:municipality:405': 1000,
                            'urn:code:municipality:007': 1000,
                        },
                        scramble_seed_key=entity['id']
                    )
                )
            ],
            oppijanumero=[
                lambda x: None
            ],
            oids=[
                lambda x: None
            ],
            dead=[
                (
                    scramble_with_weighted_pseudorandom,
                    dict(
                        key='dead',
                        weights={
                            True: 5,
                            False: 1000
                        },
                        scramble_seed_key=entity['id']
                    )
                )
            ],
            classifiedPersonInfo=[
                lambda x: None
            ],
            personalDataSafetyNonDisclosure=[
                (
                    scramble_with_weighted_pseudorandom,
                    dict(
                        key='personalDataSafetyNonDisclosure',
                        weights={
                            True: 1,
                            False: 1337,
                        },
                        scramble_seed_key=entity['id']
                    )
                )
            ],
            studentStatus=None,
            employeeStatus=None,
            identityConfirmed=[
                (
                    scramble_with_weighted_pseudorandom,
                    dict(
                        key='identityConfirmed',
                        weights={
                            True: 1337,
                            False: 2
                        },
                        scramble_seed_key=entity['id']
                    )
                )
            ],
            mergedPersonId=None,
            secondOfficialLanguageStudyObligation=[
                (
                    scramble_with_weighted_pseudorandom,
                    dict(
                        key='secondOfficialLanguageStudyObligation',
                        weights={
                            'EXEMPTION_GRANTED': 1,
                            'OBLIGATED': 100
                        },
                        scramble_seed_key=entity['id']
                    )
                )
            ],
        )

        for key, scramblers in scrambling_keys.items():
            if not scramblers:
                _out_entity[key] = entity[key]
            else:
                for _scrambler in scramblers:
                    if isinstance(_scrambler, Tuple):
                        _out_entity[key] = _scrambler[0](entity=entity, **_scrambler[1])
                    else:
                        _out_entity[key] = _scrambler(entity)

        return _out_entity
