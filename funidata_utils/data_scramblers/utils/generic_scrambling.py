import hashlib
import math
import random
import typing
from functools import lru_cache

from dateutil import rrule, parser
from pydantic import BaseModel


# Default salt for hashlib functions
DEFAULT_SALT = b"\x12D'\xf3\x95\xf3\xfe\xf0\x1ap\x8f\x89t\x07\xbf\xb8"

# used in replacing birth dates of persons
REPLACEMENT_DATES = list(rrule.rrule(rrule.DAILY,
                                     dtstart=parser.parse('1950-01-01'),
                                     until=parser.parse('2010-12-31')))


def random_shuffle(original: str, random_seed=42):
    if original is None or len(original) < 1:
        return original
    random.seed(random_seed)
    temp_list_of_str_chars = list(original)
    random.shuffle(temp_list_of_str_chars)
    return ''.join(temp_list_of_str_chars)


def _mask_range_with_value(original: str, start_index: int, end_index: int, mask_char: str):
    beginning = original[0:start_index]
    middle = mask_char * len(original[start_index:end_index + 1])
    end = original[end_index + 1:len(original)]

    return beginning + middle + end


def get_random_date(n: int | str, *args, **kwargs):
    '''
    Given input n, outputs date inside range of [1950-01-01, 2010-12-31]

    Args:
        n: integer or string used to decide scrambled date from among the all possible dates dictated by range of
        [1950-01-01, 2010-12-31].
    Returns: date inside of range [1950-01-01, 2010-12-31]
    '''
    replaced_val = replace_from_list(n, REPLACEMENT_DATES)
    return replaced_val


def replace_from_list(original_value, replacement_list):
    # Trusting in the collision resistance of SHA512 combined with using smaller replacement_list collections
    # we should be able to trust that replacement values are non-reversible
    val = replacement_list[default_hash(original_value) % len(replacement_list)]
    return val


def get_weighted_random_value(
    value_weight_dict: dict | list[tuple],
    in_seed
):
    random.seed(in_seed)
    if isinstance(value_weight_dict, list):
        values, weights = zip(*value_weight_dict)
    else:
        values, weights = zip(*value_weight_dict.items())
    return random.choices(values, weights=weights)[0]


@lru_cache(maxsize=256)
def default_hash(key, hash_function='sha512', return_int=True):
    return hashlib_hash(str(key), hash_function, return_int)


def hashlib_hash(
    key,
    hash_function,
    output_length=128,
    return_int=True,
    limit_int_len=False,
    *args,
    **kwargs
):
    if key is None:
        return None

    byt = key.encode('utf-8')

    alg = hashlib.new(hash_function)
    alg.update(byt)
    alg.update(DEFAULT_SALT)

    if return_int:
        val = int.from_bytes(alg.digest(), 'big')
        if not limit_int_len:
            return val
        return int(str(val)[0:output_length])

    return alg.hexdigest()[0:output_length]


def scramble_with_weighted_pseudorandom(
    entity: dict,
    key: str,
    weights: dict | list[tuple],
    scramble_seed_key: str | typing.Callable | None = None,
    scramble_empty_values: bool = True,
    **kwargs
):
    if isinstance(scramble_seed_key, typing.Callable):
        seed_key = scramble_seed_key(entity)
    elif scramble_seed_key:
        seed_key = scramble_seed_key
    else:
        if key not in entity:
            raise KeyError(f"Key '{key}' not in entity")

        seed_key = entity[key]

    if not entity.get(key):  # yes, this could be an oneliner, but it hurts the eyes...
        if not scramble_empty_values:
            return None

    return get_weighted_random_value(
        value_weight_dict=weights,
        in_seed=str(seed_key)
    )


def get_string_shuffled_with_mask(
    entity: dict | BaseModel | None,
    old_value_key_getter_func: typing.Callable,
    scrambling_seed=43
) -> str | None:
    if not entity:
        return None

    old_value = old_value_key_getter_func(entity)
    if not old_value or len(old_value) <= 1:
        return None

    length = len(old_value)
    return random_shuffle(
        _mask_range_with_value(old_value, math.floor(length / 2), length, '*'),
        scrambling_seed
    )
