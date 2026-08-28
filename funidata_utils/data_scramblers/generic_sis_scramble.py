from typing import Tuple, Callable

from funidata_utils.data_scramblers.base import SingletonMetaScrambler
from funidata_utils.utils import update_inner_dictionary_key


class SisMetadataScrambler(SingletonMetaScrambler):
    @classmethod
    def scramble(cls, entity: dict, processed_keys: dict) -> dict:
        """ only scrambles metadata and leaves rest of entity intact """
        scrambling_keys = dict(
            metadata=[
                (
                    update_inner_dictionary_key,
                    dict(
                        dot_separated_key='metadata.createdBy',
                        new_value='Lorem'
                    )
                ),
                (
                    update_inner_dictionary_key,
                    dict(
                        dot_separated_key='metadata.lastModifiedBy',
                        new_value='Ipsum'
                    )
                ),
            ],
        )

        for key, scramblers in scrambling_keys.items():
            processed_keys[key].append(scramblers)
            if not scramblers:
                continue

            for _scrambler in scramblers:
                if isinstance(_scrambler, Tuple):
                    entity[key] = _scrambler[0](entity=entity, **_scrambler[1])
                elif isinstance(_scrambler, Callable):
                    entity[key] = _scrambler(entity)
                else:
                    raise Exception("Unknown scrambler dict formatting")
        return entity


class UnprocessedKeysDropperScrambler(SingletonMetaScrambler):
    def __init__(self, loggable_keys: set[str]):
        self._loggable_keys = loggable_keys

    # Instance method to provide access to self._loggable_keys
    def scramble(self, entity: dict, processed_keys: dict) -> dict:
        """ Pops any keys that are not present in processed_keys """
        entity_keys = set(entity.keys())
        _keys = set()
        for key in entity_keys:
            if key not in processed_keys:
                _keys.add(key)
                entity.pop(key)

        _keys_diff = _keys.difference(self._loggable_keys)
        if _keys_diff:
            self._loggable_keys |= _keys_diff

        return entity
