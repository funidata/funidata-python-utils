from functools import lru_cache
from typing import Tuple


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class SingletonMetaScrambler(metaclass=SingletonMeta):
    scrambling_keys: dict

    @classmethod
    @lru_cache
    def keys_without_scrambling(cls):
        return {k for k, v in getattr(cls, 'scrambling_keys', {}).items() if not v}

    @classmethod
    @lru_cache
    def dict_items_with_scrambling(cls):
        return {
            k: v
            for k, v in getattr(cls, 'scrambling_keys', {}).items()
            if v
        }.items()

    @classmethod
    def scramble(cls, entity: dict, processed_keys: set) -> dict:
        """ Scramble the entity and update processed_keys """
        processed_keys |= cls.keys_without_scrambling()

        for key, scramblers in cls.dict_items_with_scrambling():
            if key not in entity:
                continue

            processed_keys.add(key)

            for _scrambler in scramblers:
                if isinstance(_scrambler, Tuple):
                    entity[key] = _scrambler[0](entity=entity, **_scrambler[1])
                else:
                    entity[key] = _scrambler(entity)

        return entity
