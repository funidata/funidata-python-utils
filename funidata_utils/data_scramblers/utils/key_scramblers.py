import typing

from pydantic import BaseModel

from funidata_utils.data_scramblers.replacement_data import first_names, last_names
from funidata_utils.data_scramblers.utils.generic_scrambling import (
    replace_from_list, scramble_with_weighted_pseudorandom,
    get_string_shuffled_with_mask, get_weighted_random_value,
)


def get_scrambled_email(
    entity: dict | BaseModel | None = None,
    hash_key_getter_func: typing.Callable = lambda x: x['id'],
    *args,
    **kwargs
) -> str | None:
    if not entity:
        return None

    return f"email-{hash_key_getter_func(entity)}@scrambled.fi"


def get_scrambled_first_name(
    entity: dict | BaseModel | None = None,
    hash_key_getter_func: typing.Callable = lambda x: x['id'],
    old_value_key_getter_func: typing.Callable = lambda x: x.get('firstNames'),
    *args,
    **kwargs
) -> str | None:
    if not entity:
        return None

    first_name_list = first_names
    old_value = old_value_key_getter_func(entity)

    return replace_from_list(hash_key_getter_func(entity), first_name_list) if old_value else old_value


def get_phone_number_shuffled_with_mask(
    entity: dict | BaseModel | None = None,
    seed_getter_func: typing.Callable = lambda x: x['id'],
    old_value_key_getter_func: typing.Callable = lambda x: x.get('phoneNumber'),
    *args,
    **kwargs
) -> str | None:
    return get_string_shuffled_with_mask(
        entity,
        old_value_key_getter_func,
        scrambling_seed=seed_getter_func(entity)
    )


def get_scrambled_last_name(
    entity: dict | BaseModel | None = None,
    hash_key_getter_func: typing.Callable = lambda x: x['id'],
    old_value_key_getter_func: typing.Callable = lambda x: x.get('lastName'),
    *args,
    **kwargs
) -> str | None:
    if not entity:
        return None

    last_name_list = last_names
    old_value = old_value_key_getter_func(entity)

    return replace_from_list(hash_key_getter_func(entity), last_name_list) if old_value else old_value


def get_scrambled_nationalities(
    entity: dict,
    *args,
    **kwargs
):
    if not entity.get('citizenshipUrns'):
        return entity.get('citizenshipUrns')

    random_nationality_count = get_weighted_random_value(
        value_weight_dict={
            1: 100,
            2: 1
        },
        in_seed=str(entity['id'])
    )
    if random_nationality_count > 1:
        # TODO: figure out a more robust way later in case of triple/quadruple nationalitites are required
        return [
            scramble_with_weighted_pseudorandom(
                entity=entity,
                key='citizenshipUrns',
                weights={
                    k: v for k, v in {
                        'urn:code:country:246': 5000,
                        'urn:code:country:248': 50,
                        'urn:code:country:752': 25,
                        'urn:code:country:056': 10,
                        'urn:code:country:276': 10,
                        'urn:code:country:250': 10,
                    }.items() if k != x
                },
                scramble_seed_key=str(entity['id']) + x
            )
            for x in entity.get('citizenshipUrns')
        ]

    return [
        scramble_with_weighted_pseudorandom(
            entity=entity,
            key='citizenshipUrns',
            weights={
                'urn:code:country:246': 5000,
                'urn:code:country:248': 50,
                'urn:code:country:752': 25,
                'urn:code:country:056': 10,
                'urn:code:country:276': 10,
                'urn:code:country:250': 10,
            },
            scramble_seed_key=str(entity['id'])
        )
    ]
